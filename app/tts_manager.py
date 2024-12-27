import asyncio


class TTSManager:
    def __init__(self, model_checkpoint):
        self.model_checkpoint = model_checkpoint
        self.process = None

    async def start_process(self, text):
        if self.process is None:
            cmd = ["piper-cli", "--model", self.model_checkpoint, "--output_file", "-", "--cuda"]

            self.process = await asyncio.create_subprocess_exec(
                    *cmd,
                    stdin=asyncio.subprocess.PIPE,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
            )

    async def get_output(self, text):
        if self.process is None:
            await self.start_process()

        stdout, stderr = await self.process.communicate(input=text.encode())

        return stdout

