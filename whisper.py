from openai import OpenAI

class WhisperClient:
    def __init__(self, model="Systran/faster-whisper-small", 
                 api_key="cant-be-empty", base_url="http://localhost:8000/v1/"):
        self.model = model
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def transcribe(self, file):
        transcript = self.client.audio.transcriptions.create(
            model=self.model, file=file
        )
        return transcript.text