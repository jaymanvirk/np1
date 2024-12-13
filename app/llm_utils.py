import asyncio
from llm_manager import ollama_manager
import time
import json

async def send_input_to_ollama(model_name: str, str_input: str):
    """Send user input to the Ollama process."""
    await ollama_manager.start_process(model_name)
    await ollama_manager.send_input(model_name, str_input)

async def stream_llm_output(websocket, model_name: str, stt_manager):
    """Function to stream output from the Ollama subprocess."""
    await send_input_to_ollama(model_name, stt_manager.transcription)
    m_id = int(time.time())
    flag = False
    async for output in ollama_manager.get_output(model_name):
        flag = True
        message = {
            "sender": {
                "name": "K"
            },
            "meta": {
                "id": m_id
            },
            "media": {
                "text": output 
            }
        }
        await websocket.send_text(json.dumps(message))
    
    if flag:
        async with stt_manager.lock:
            stt_manager.id += 1
            stt_manager.combined_audio = stt_manager.audio_chunk_0
