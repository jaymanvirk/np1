import asyncio
import json
from typing import Optional, Dict, Any


class PiperTTS:
    def __init__(self, piper_path: str, model_path: str, gpu_device: int):
        self.piper_path = piper_path
        self.model_path = model_path
        self.gpu_device = gpu_device
        self.process: Optional[asyncio.subprocess.Process] = None
        self.input_queue: asyncio.Queue[Optional[Dict[str, Any]]] = asyncio.Queue()
        self.output_queue: asyncio.Queue[bytes] = asyncio.Queue()

    async def start(self):
        cmd = [
            self.piper_path,
            "--model", self.model_path,
            "--output-raw",
            "--cuda",
            "--gpu-device", str(self.gpu_device),
            "--json-input"
        ]
        self.process = await asyncio.create_subprocess_exec(
            *cmd,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.DEVNULL
        )
        asyncio.create_task(self.process_input())
        asyncio.create_task(self.process_output())

    async def process_input(self):
        assert self.process and self.process.stdin
        try:
            while True:
                input_data = await self.input_queue.get()
                if input_data is None:
                    break
                self.process.stdin.write(json.dumps(input_data).encode() + b'\n')
                await self.process.stdin.drain()
        finally:
            self.process.stdin.close()

    async def process_output(self):
        assert self.process and self.process.stdout
        try:
            while True:
                audio_chunk = await self.process.stdout.read(4096)
                if not audio_chunk:
                    break
                await self.output_queue.put(audio_chunk)
        finally:
            await self.output_queue.put(b'')  # Signal end of output

    async def generate_speech(self, text: str, speaker_id: int = 0):
        input_data = {
            "text": text,
            "speaker_id": speaker_id,
            "length_scale": 1.0,
            "noise_scale": 0.667,
            "noise_w": 0.8
        }
        await self.input_queue.put(input_data)

    async def get_audio_chunk(self) -> bytes:
        return await self.output_queue.get()

    async def close(self):
        await self.input_queue.put(None)
        if self.process:
            try:
                await asyncio.wait_for(self.process.wait(), timeout=5.0)
            except asyncio.TimeoutError:
                self.process.kill()
            finally:
                self.process = None


piper_tts = PiperTTS()

