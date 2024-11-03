import asyncio
from ollama_manager import ollama_manager


async def send_input_to_ollama(model_name: str, str_input: str):
    """Send user input to the Ollama process."""
    process = ollama_manager.start_process(model_name)
    process.stdin.write(str_input + '\n')
    process.stdin.flush()
    return process


async def get_response(process):
    """Function to get response from a process."""
    loop = asyncio.get_running_loop()
    output = await loop.run_in_executor(None, process.stdout.readline)
    return output.strip() if output else None


async def stream_ollama_output(websocket, process):
    """Function to stream output from the Ollama subprocess."""
    try:
        while True:
            output = await get_response(process)
            if output:
                await websocket.send_text(output.strip())
            else:
                break
    except Exception as e:
        await websocket.send_text(f"Error while reading output: {e}")


async def process_ollama_request(websocket, model_name: str, str_input: str):
    """Process a single Ollama request."""
    process = await send_input_to_ollama(model_name, str_input)
    await stream_ollama_output(websocket, process)


async def is_thought_complete(str_input: str):
    """Function to check if the input thought is complete"""
    prompt = '''
                Is the thought of the following sentence complete?
                Answer "YES" if complete otherwise answer "NO".
                Here is the sentence:
            '''
    prompt += str_input

    process = await send_input_to_ollama(model_name, str_input)

    return await get_response(process)
