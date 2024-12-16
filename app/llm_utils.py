import asyncio
from llm_manager import ollama_manager
import time
import json


async def stream_llm_output(websocket, model_name: str, stt_manager):
    """Function to stream output from the Ollama subprocess."""
    m_id = int(time.time())
    flag = False
    async for output in ollama_manager.chat(stt_manager.transcription):
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
            stt_manager.audio_bytes = b''
