import asyncio


class TTSManager:
    def __init__(self):
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

    async def get_output(self, text, model_checkpoint):
        await self.start_process(model_checkpoint)
        process = self.processes[model_checkpoint]

        stdout, stderr = await process.communicate(input=text.encode())

        return stdout

    async def close(self):
        for model_checkpoint, process in self.processes.items():
            process.terminate()
            await process.wait()

        self.processes.clear()

