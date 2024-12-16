import aiohttp
import json
from typing import AsyncGenerator, List


class OllamaManager:
    def __init__(self, url: str, model_name: str):
        self.url = url
        self.model_name = model_name
        self.messages: List[dict] = []
        
    def add_message(self, role: str, content: str):
        """Store a user message."""
        message = {"role": role, "content": content}
        self.messages.append(message)

    async def start_session(self) -> None:
        """Start up the Ollama session"""
        test_message = "Instruction"
        async for _ in self.chat(test_message):
            pass

    async def chat(self, content: str) -> AsyncGenerator[str, None]:
        """Send a message to the model and return an async generator of responses."""
        self.add_message("user", content)
        
        assistant_message = ""
        async with aiohttp.ClientSession() as session:
            async with session.post(self.url, json={"model": self.model_name, "messages": self.messages}) as response:
                if response.status == 200:
                    async for line in response.content:
                        output_line = line.decode().strip()
                        if output_line:
                            output = json.loads(output_line)
                            assistant_message += str(output["message"]["content"])
                            yield assistant_message

        self.add_message("assistant", assistant_message)
