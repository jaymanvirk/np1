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


async def stream_ollama_output(websocket, str_input: str):
    """Function to stream output from the Ollama subprocess."""
    try:
        process = await send_input_to_ollama(model_name, str_input)
        while True:
            output = await get_response(process)
            if output:
                output = output.replace("\"", "\\\"")
                await websocket.send_text(f'{{"sender":{{"name":"K"}}, "media":{{"text": {output}}}}}') 
            else:
                break
    except Exception as e:
        await websocket.send_text(f"Error while reading output: {e}")


async def is_thought_complete(model_name, str_input: str):
    """Function to check if the input thought is complete"""
    intsruction = '''
                Answer "True" or "False" to the following question:
                Is the thought of the following sentence complete?
                Sentence: 
            '''
    prompt = instruction + str_input

    process = await send_input_to_ollama(model_name, prompt)

    return await get_response(process)
