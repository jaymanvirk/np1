from fastapi import WebSocket, APIRouter
from queue_utils import process_queue
from stt_manager import STTManager 
from llm_manager import OllamaManager 
import asyncio
import os

OLLAMA_URL = os.getenv("OLLAMA_URL")
LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME")

router = APIRouter()

@router.websocket("/v1/audio")
async def handle_stream_audio(websocket: WebSocket):
    await websocket.accept()
    queue = asyncio.Queue()
    stt_manager = STTManager()
   
    ollama_manager = OllamaManager(OLLAMA_URL, LLM_MODEL_NAME)
    await ollama_manager.start_session()

    stream_task = asyncio.create_task(process_queue(websocket, queue, stt_manager, ollama_manager))

    try:
        stt_manager.audio_chunk_0 = await websocket.receive_bytes()
        while True:
            audio_chunk = await websocket.receive_bytes()
            await queue.put(audio_chunk)
    finally:
        stream_task.cancel()
        await ollama_manager.close_session()
        await websocket.close()

