import asyncio
import json
from typing import Optional, Dict, Any, AsyncGenerator

class OllamaManager:
    def __init__(self):
        self.processes: Dict[str, asyncio.subprocess.Process] = {}
        self.input_queues: Dict[str, asyncio.Queue[Optional[str]]] = {}
        self.output_queues: Dict[str, asyncio.Queue[str]] = {}

    async def start_process(self, model_name: str):
        if model_name not in self.processes:
            ollama_command = f"ollama run {model_name}"
            process = await asyncio.create_subprocess_exec(
                *ollama_command.split(),
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            self.processes[model_name] = process
            self.input_queues[model_name] = asyncio.Queue()
            self.output_queues[model_name] = asyncio.Queue()
            
            asyncio.create_task(self.process_input(model_name))
            asyncio.create_task(self.process_output(model_name))
        
        return self.processes[model_name]

    async def process_input(self, model_name: str):
        process = self.processes[model_name]
        input_queue = self.input_queues[model_name]
        assert process.stdin
        try:
            while True:
                input_data = await input_queue.get()
                if input_data is None:
                    break
                process.stdin.write((input_data + '\n').encode())
                await process.stdin.drain()
        finally:
            process.stdin.close()

    async def process_output(self, model_name: str):
        process = self.processes[model_name]
        output_queue = self.output_queues[model_name]
        assert process.stdout
        try:
            while True:
                line = await process.stdout.readline() 
                if not line:
                    break
                decoded_line = line.strip().decode()
                if decoded_line:
                    await output_queue.put(decoded_line)
        except Exception as e:
            await output_queue.put({"process_output":str(e)})

    async def send_input(self, model_name: str, input_text: str):
        if model_name in self.input_queues:
            await self.input_queues[model_name].put(input_text)

    async def get_output(self, model_name: str) -> AsyncGenerator[str, None]:
        if model_name in self.input_queues:
            try:
                while True:
                    output = await self.output_queues[model_name].get()
                    yield output
            except Exception as e:
                yield {"get_output": str(e)}

    async def stop_process(self, model_name: str):
        if model_name in self.processes:
            process = self.processes[model_name]
            await self.input_queues[model_name].put(None)
            try:
                await asyncio.wait_for(process.wait(), timeout=5.0)
            except asyncio.TimeoutError:
                process.kill()
            finally:
                del self.processes[model_name]
                del self.input_queues[model_name]
                del self.output_queues[model_name]

ollama_manager = OllamaManager()

