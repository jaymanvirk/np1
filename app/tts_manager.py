import asyncio
import subprocess
import json
from asyncio import Queue
from threading import Thread

class PiperTTS:
    def __init__(self):
        self.process = None
        self.input_queue = Queue()
        self.output_queue = Queue()
        self.start_piper_process()

    def start_piper_process(self):
        cmd = [
            PIPER_PATH,
            "--model", MODEL_PATH,
            "--output-raw",
            "--cuda",
            "--gpu-device", str(GPU_DEVICE),
            "--json-input"
        ]
        self.process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL
        )
        Thread(target=self.process_input).start()
        Thread(target=self.process_output).start()

    def process_input(self):
        while True:
            input_data = self.input_queue.get()
            if input_data is None:
                break
            self.process.stdin.write(json.dumps(input_data).encode() + b'\n')
            self.process.stdin.flush()

    def process_output(self):
        while True:
            audio_chunk = self.process.stdout.read(4096)
            if not audio_chunk:
                break
            self.output_queue.put(audio_chunk)

    def generate_speech(self, text, speaker_id=0):
        input_data = {
            "text": text,
            "speaker_id": speaker_id,
            "length_scale": 1.0,
            "noise_scale": 0.667,
            "noise_w": 0.8
        }
        self.input_queue.put(input_data)

    def get_audio_chunk(self):
        return self.output_queue.get()

    def close(self):
        self.input_queue.put(None)
        self.process.stdin.close()
        self.process.stdout.close()
        self.process.wait()

piper_tts = PiperTTS()
