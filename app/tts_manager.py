import asyncio
import os


class TTSManager:
    def __init__(self):
        self.model_dir = f'{os.getenv("MC_DIR")}/{os.getenv("TTS_DIR")}' 
        self.processes = {}

    async def start_process(self, model_checkpoint):
        if model_checkpoint not in self.processes:
            cmd = ["piper-cli", "--model", model_checkpoint, "--output_file", "-", "--cuda"]

            process = await asyncio.create_subprocess_exec(
                    *cmd,
                    stdin=asyncio.subprocess.PIPE,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
            )
            self.processes[model_checkpoint] = process

    async def get_output(self, text, model_name):
        model_checkpoint = f'{self.model_dir}/{model_name}.onnx'
        await self.start_process(model_checkpoint)
        process = self.processes[model_checkpoint]

        stdout, stderr = await process.communicate(input=text.encode())

        return stdout

    async def close(self):
        for model_checkpoint, process in self.processes.items():
            process.terminate()
            await process.wait()

        self.processes.clear()

