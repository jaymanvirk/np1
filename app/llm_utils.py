import asyncio
from llm_manager import ollama_manager
import time
import json

async def send_input_to_ollama(model_name: str, str_input: str):
    """Send user input to the Ollama process."""
    await ollama_manager.start_process(model_name)
    await ollama_manager.send_input(model_name, str_input)

async def stream_ollama_output(websocket, model_name: str, str_input: str):
    """Function to stream output from the Ollama subprocess."""
    try:
        await send_input_to_ollama(model_name, str_input)
        while True:
            response = await ollama_manager.get_output(model_name)
            if response:
                m_id = int(time.time())
                message = {
                    "sender": {
                        "name": "K"
                    },
                    "meta": {
                        "id": m_id
                    },
                    "media": {
                        "text": response
                    }
                }
                await websocket.send_text(json.dumps(message))
            else:
                break
    except Exception as e:
        await websocket.send_text(f"Error while reading output: {e}")

async def is_thought_complete(model_name: str, str_input: str):
    """Function to check if the input thought is complete"""
    instruction = '''
                Answer "True" or "False" to the following question:
                Is the thought of the following sentence complete?
                Sentence: 
            '''
    prompt = instruction + str_input

    await send_input_to_ollama(model_name, prompt)
    return await ollama_manager.get_output(model_name)

