from fastapi import WebSocket, APIRouter
from queue_utils import process_queue
from stt_manager import STTManager 
from llm_manager import ollama_manager
import asyncio
import os


LLM_CHECKPOINT = os.getenv("LLM_CHECKPOINT")

router = APIRouter()

@router.websocket("/v1/audio")
async def handle_stream_audio(websocket: WebSocket):
    await websocket.accept()
    queue = asyncio.Queue()
    stt_manager = STTManager()
    
    await ollama_manager.start_session()

    stream_task = asyncio.create_task(process_queue(websocket, queue, stt_manager))

    try:
        stt_manager.audio_chunk_0 = await websocket.receive_bytes()
        while True:
            audio_chunk = await websocket.receive_bytes()
            await queue.put(audio_chunk)
    finally:
        stream_task.cancel()
        await ollama_manager.stop_process(LLM_CHECKPOINT)
        await websocket.close()

