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
    await send_input_to_ollama(model_name, str_input)
    m_id = int(time.time())
    while True:
        response = await ollama_manager.get_output(model_name)
        if response:
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

