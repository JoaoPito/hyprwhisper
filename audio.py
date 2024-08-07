import pyaudio
import wave
import numpy as np

def calculate_amplitude(audio_data):
    """Calculates the amplitude of audio data.

    Args:
        audio_data: A NumPy array containing the audio data.

    Returns:
        The average amplitude of the audio data.
    """
    audio_data = audio_data.astype(np.float32)
    absolute_values = np.abs(audio_data)
    amplitude = np.mean(absolute_values)
    return amplitude

CHANNELS = 1

class Recorder:
    def __init__(self, rate=44100, format=pyaudio.paInt16, framesize=1024):
        self.frames = []
        self.rate = rate
        self.format = format
        self.stream = None
        self.is_recording = False
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=self.format,
                            channels=CHANNELS,
                            rate=self.rate,
                            input=True,
                            frames_per_buffer=framesize)

    def record_audio_frame(self, framesize=1024):
        self.is_recording = True
        data = self.stream.read(framesize)
        self.frames.append(data)
    
    def stop_recording(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        self.is_recording = False

    def save_to_file(self, filepath):
        if self.is_recording:
            self.stop_recording()
        wf = wave.open(filepath, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.audio.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(self.frames))
        wf.close()