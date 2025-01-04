import asyncio
import os


class TTSManager:
    def __init__(self):
        self.model_dir = f'{os.getenv("MC_DIR")}/{os.getenv("TTS_DIR")}'

    async def get_output(self, text, model_name):
        model_checkpoint = f'{self.model_dir}/{model_name}.onnx'
        cmd = ["piper-cli", "--model", model_checkpoint, "--output_file", "-", "--cuda"]

        process = await asyncio.create_subprocess_exec(
                *cmd,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate(input=text.encode())

        return stdout
