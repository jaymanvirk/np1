import asyncio


class TTSManager:
    def __init__(self, model_checkpoint):
        self.model_checkpoint = model_checkpoint

    async def get_output(self, text):
        cmd = ["piper-cli", "--model", self.model_checkpoint, "--output_file", "-", "--cuda"]

        process = await asyncio.create_subprocess_exec(
                *cmd,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate(input=text.encode())

        return stdout

