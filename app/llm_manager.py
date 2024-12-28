import aiohttp
import json
from typing import AsyncGenerator, List


class LLMManager:
    def __init__(self, url: str, model_name: str):
        self.url = url
        self.model_name = model_name
        self.messages: List[dict] = []
        self.session: aiohttp.ClientSession = None        

    def add_message(self, role: str, content: str):
        """Store a user message."""
        if content:
            message = {"role": role, "content": content}
            self.messages.append(message)

    async def start_session(self) -> None:
        """Start up the Ollama session"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()

        start_message = ""
        async for _ in self.chat(start_message):
            pass

    async def chat(self, content: str) -> AsyncGenerator[str, None]:
        """Send a message to the model and return an async generator of responses."""
        try:
            self.add_message("user", content)
            buffer_response = ""
            async with self.session.post(self.url, json={"model": self.model_name, "messages": self.messages}) as response:
                if response.status == 200:
                    async for line in response.content:
                        output_line = line.decode().strip()
                        if output_line:
                            output = json.loads(output_line)
                            output = str(output["message"]["content"])
                            buffer_response += output
                            yield output
        finally:
            self.add_message("assistant", buffer_response)

    async def close(self) -> None:
        """Close the aiohttp ClientSession"""
        if self.session and not self.session.closed:
            await self.session.close()       

