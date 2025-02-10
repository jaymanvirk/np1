import aiohttp
import json
from typing import AsyncGenerator, List
import os


class LLMManager:
    def __init__(
                   self
                 , url=os.getenv("OLLAMA_URL")
                 , model_checkpoint=os.getenv("LLM_CHECKPOINT")
                 , model_checkpoint_embed=os.getenv("EMBED_CHECKPOINT")
                 , instruction_gen=os.getenv("LLM_INSTRUCTION_GEN")
                 ):
        self.url_chat = f'{url}/chat'
        self.url_embeddings = f'{url}/embeddings'
        self.url_generate = f'{url}/generate'
        self.model_checkpoint = model_checkpoint
        self.model_checkpoint_embed = model_checkpoint_embed
        self.instruction_gen = instruction_gen
        self.messages: List[dict] = []
        self.session = aiohttp.ClientSession() 

    def add_message(self, role: str, content: str):
        """Store a user message."""
        if content:
            message = {"role": role, "content": content}
            self.messages.append(message)

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
    
    async def get_embedding(self, prompt):
        headers = {'Content-Type': 'application/json'}
        payload = {
            "model": self.model_checkpoint_embed
            ,"prompt": prompt
        }

        async with self.session.post(self.url_embedddings, headers=headers, data=json.dumps(payload)) as response:
            if response.status == 200:
                result = await response.json()

                return result["embedding"]
     
    async def get_query(self, prompt):
        full_prompt = f'{self.instruction_gen}\n\n{prompt}'
        headers = {'Content-Type': 'application/json'}
        payload = {
            "model": self.model_checkpoint
            ,"prompt": full_prompt
            ,"stream": False
        }

        async with self.session.post(self.url_embeddings, headers=headers, data=json.dumps(payload)) as response:
            if response.status == 200:
                result = await response.json()

                return result["response"]
            
    async def get_generate(self, prompt):
        headers = {'Content-Type': 'application/json'}
        payload = {
            "model": self.model_checkpoint
            ,"prompt": prompt
            ,"stream": True
        }
        async with self.session.post(self.url_generate, headers=headers, data=json.dumps(payload)) as response:
            if response.status == 200:
                async for line in response.content:
                    output_line = line.decode().strip()
                    if output_line:
                        output = json.loads(output_line)
                        yield str(output["response"])

    async def close(self) -> None:
        """Close the aiohttp ClientSession"""
        if self.session and not self.session.closed:
            await self.session.close()       

