from datetime import datetime, timedelta
import os
import queue
from flask import Flask
import threading

from dotenv import load_dotenv
from audio import Recorder
from google_llm import GoogleLLM
from whisper import WhisperClient

load_dotenv()

# CONFIG
CONTEXT_TIMEOUT_MIN = 1
TEMPORARY_DIR_VAR = "TEMP_FOLDER"

# Assign tools to LLM
from tools.screenshot import get_screenshot
from tools.clipboard import paste_from_clipboard, copy_to_clipboard

tools = [get_screenshot, paste_from_clipboard, copy_to_clipboard]
llm = GoogleLLM(model_name="gemini-1.5-pro", tools=tools)

whisper = WhisperClient()

app = Flask(__name__)

last_request = datetime.now()
is_recording = False
flag_lock = threading.Lock()

def service(q: queue.Queue):
    global is_recording
    
    audio_recorder = Recorder()
    recording_filepath = os.path.join(os.getenv(TEMPORARY_DIR_VAR), f"rec_{datetime.now().strftime("%d%m%y_%H%M%S")}.wav")

    print("> Recording")
    while True:
        with flag_lock:
            if not is_recording:
                print("Done")
                break
        print(".", end='', flush=True)
        audio_recorder.record_audio_frame()
            
    audio_recorder.save_to_file(recording_filepath)
    print("> Transcribing")
    transcription = whisper.transcribe(open(recording_filepath, "rb"))
    print(f"'{transcription}'")
    os.remove(recording_filepath)
    
    print(f"> LLM")
    global last_request
    
    if(datetime.now() - last_request >= timedelta(minutes=CONTEXT_TIMEOUT_MIN)):
        llm.clear_chat()
        print("=> Chat cleared")
    
    last_request = datetime.now()
    llm_response = llm.invoke(transcription)
    print(llm_response)
    copy_to_clipboard(llm_response)
    q.put(llm_response)
    
service_thread = None
service_queue = None
def start_service():
    global service_thread
    global service_queue
    if service_thread == None:
        service_queue = queue.Queue()
        service_thread = threading.Thread(target=service, args=(service_queue,))
        print("Starting...")
        service_thread.start()
        return "Recording\n"
    else:
        service_thread.join()
        service_thread = None
        return service_queue.get()

@app.route('/')
def toggle():
    global is_recording
    with flag_lock:
        is_recording = not is_recording
    service_result = start_service()
    return f"> {service_result}"

if __name__ == '__main__':
    app.run(debug=True)
