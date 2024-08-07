from datetime import datetime, timedelta
import os
from flask import Flask
import threading

from dotenv import load_dotenv
from audio import Recorder
from google_llm import GoogleLLM
from whisper import WhisperClient

load_dotenv()

# CONFIG
CONTEXT_TIMEOUT_MIN = 30

# Assign tools to LLM
from tools.screenshot import get_screenshot

tools = [get_screenshot]
llm = GoogleLLM(tools=tools)

whisper = WhisperClient()

app = Flask(__name__)

last_request = datetime.now()
is_recording = False
flag_lock = threading.Lock()

def service():
    global is_recording
    
    audio_recorder = Recorder()
    filepath = f"./temp_recording_{datetime.now().strftime("%d%m%y_%H%M%S")}.wav"

    print("> Recording")
    while True:
        with flag_lock:
            if not is_recording:
                print("Done")
                break
        print(".", end='', flush=True)
        audio_recorder.record_audio_frame()
            
    audio_recorder.save_to_file(filepath)
    print("> Transcribing")
    transcription = whisper.transcribe(open(filepath, "rb"))
    print(f"> '{transcription}'")
    
    print(f"> LLM")
    global last_request
    
    if(datetime.now() - last_request >= timedelta(minutes=CONTEXT_TIMEOUT_MIN)):
        llm.clear_chat()
    
    last_request = datetime.now()
    llm_response = llm.invoke(transcription)
    print(llm_response)
    
    # IF THERE PARAMETER --transcript IS NOT SET:
        # Send results to googlellm
        # Any results from LLM print to the user (or speak)
    # IF PARAMETER IS SET:
        # Using clipboard tool, copy transcript
    
    os.remove(filepath)

def start_service():
    service_thread = threading.Thread(target=service)
    service_thread.daemon = True
    service_thread.start()

@app.route('/')
def toggle():
    global is_recording
    with flag_lock:
        is_recording = not is_recording
        if(is_recording):
            start_service()
    return "> Recording\n" if is_recording else "> Transcribing\n"

if __name__ == '__main__':
    app.run(debug=True)
