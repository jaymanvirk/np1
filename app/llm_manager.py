import aiohttp
import json
from typing import AsyncGenerator, List
import os

OLLAMA_URL = os.getenv("OLLAMA_URL")
LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME")

class OllamaManager:
    def __init__(self, url: str, model_name: str):
        self.url = url
        self.model_name = model_name
        self.messages: List[dict] = []
        self.session: aiohttp.ClientSession = None        

    def add_message(self, role: str, content: str):
        """Store a user message."""
        message = {"role": role, "content": content}
        self.messages.append(message)

    async def start_session(self) -> None:
        """Start up the Ollama session"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()

        test_message = "Instruction"
        async for _ in self.chat(test_message):
            pass

    async def chat(self, content: str) -> AsyncGenerator[str, None]:
        """Send a message to the model and return an async generator of responses."""
        self.add_message("user", content)
        
        assistant_message = ""
        async with self.session.post(self.url, json={"model": self.model_name, "messages": self.messages}) as response:
            if response.status == 200:
                async for line in response.content:
                    output_line = line.decode().strip()
                    if output_line:
                        output = json.loads(output_line)
                        assistant_message += str(output["message"]["content"])
                        yield assistant_message

        self.add_message("assistant", assistant_message)

    async def close_session(self) -> None:
        """Close the aiohttp ClientSession"""
        if self.session and not self.session.closed:
            await self.session.close()       

ollama_manager = OllamaManager(OLLAMA_URL, LLM_MODEL_NAME)

