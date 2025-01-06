import aiohttp
import json
from typing import AsyncGenerator, List


class LLMManager:
    def __init__(self, url: str, model_checkpoint: str, model_checkpoint_embed: str, instrucion_gen: str):
        self.url_chat = f'{url}/chat'
        self.url_embed = f'{url}/embeddings'
        self.url_gen = f'{url}/generate'
        self.model_checkpoint = model_checkpoint
        self.model_checkpoint_embed = model_checkpoint_embed
        self.instruction_gen = instruction_gen
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

    async def get_chat(self, content: str) -> AsyncGenerator[str, None]:
        """Send a message to the model and return an async generator of responses."""
        try:
            self.add_message("user", content)
            buffer_response = ""
            async with self.session.post(self.url_chat, json={"model": self.model_checkpoint, "messages": self.messages}) as response:
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
    
    async def get_embedding(prompt):
        headers = {'Content-Type': 'application/json'}
        payload = {
            "model": self.model_checkpoint_embed
            ,"prompt": prompt
        }

        async with self.session.post(self.url_embed, headers=headers, data=json.dumps(payload)) as response:
            if response.status == 200:
                result = await response.json()

                return result["embedding"]
     
    async def get_query(prompt):
        full_prompt = f'{self.instruction_gen}\n\n{prompt}'
        headers = {'Content-Type': 'application/json'}
        payload = {
            "model": self.model_checkpoint
            ,"prompt": full_prompt
            ,"stream": False
        }

        async with self.session.post(self.url_embed, headers=headers, data=json.dumps(payload)) as response:
            if response.status == 200:
                result = await response.json()

                return result["response"]
    
    async def close(self) -> None:
        """Close the aiohttp ClientSession"""
        if self.session and not self.session.closed:
            await self.session.close()       

