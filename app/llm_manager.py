import asyncio
from typing import Optional, Dict, Any, AsyncGenerator, List

class OllamaManager:
    def __init__(self):
        self.processes: Dict[str, asyncio.subprocess.Process] = {}
        self.input_queues: Dict[str, asyncio.Queue[Optional[str]]] = {}
        self.output_queues: Dict[str, asyncio.Queue[str]] = {}
        self.tasks: Dict[str, List[asyncio.Task]] = {}

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
            
            task_input = asyncio.create_task(self.process_input(model_name))
            task_output = asyncio.create_task(self.process_output(model_name))
            self.tasks[model_name] = [task_input, task_output]

        return self.processes[model_name]

    async def process_input(self, model_name: str):
        process = self.processes[model_name]
        input_queue = self.input_queues[model_name]
        assert process.stdin
        try:
            while True:
                input_data = await input_queue.get()
                if input_data:
                    process.stdin.write((input_data + '\n').encode())
                    await process.stdin.drain()

    async def process_output(self, model_name: str):
        process = self.processes[model_name]
        output_queue = self.output_queues[model_name]
        assert process.stdout
        try:
            flag = False
            while True:
                line = await process.stdout.readline() 
                if line:
                    decoded_line = line.strip().decode()
                    if decoded_line:
                        flag = True
                        await output_queue.put(decoded_line)
                elif flag:
                    flag = False
                    await output_queue.put(None)
        except Exception as e:
            await output_queue.put(f"process_output: {str(e)}")

    async def send_input(self, model_name: str, input_text: str):
        if model_name in self.input_queues:
            await self.input_queues[model_name].put(input_text)

    async def get_output(self, model_name: str) -> AsyncGenerator[str, None]:
        if model_name in self.input_queues:
            output_queue = self.output_queues[model_name]
            try:
                while True:
                    output = await output_queue.get()
                    if output is None:
                        break
                    yield output
            except Exception as e:
                yield f"get_output: {str(e)}"

    async def stop_process(self, model_name: str):
        if model_name in self.processes:
            for task in self.tasks.get(model_name, []):
                task.cancel()
            
            process = self.processes[model_name]
            process.terminate()
            try:
                await asyncio.wait_for(process.wait(), timeout=1.0)
            except asyncio.TimeoutError:
                process.kill()
            del self.processes[model_name]
            del self.input_queues[model_name]
            del self.output_queues[model_name]
            del self.tasks[model_name]

ollama_manager = OllamaManager()

