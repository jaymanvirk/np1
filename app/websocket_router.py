from fastapi import WebSocket, APIRouter
from queue_utils import process_queue
from stt_manager import STTManager 
from llm_manager import LLMManager 
from tts_manager import TTSManager
import asyncio
import os

router = APIRouter()

@router.websocket("/v1/audio")
async def handle_stream_audio(websocket: WebSocket):
    await websocket.accept()
    queue = asyncio.Queue()

    OLLAMA_URL = os.getenv("OLLAMA_URL")
    LLM_CHECKPOINT = os.getenv("LLM_CHECKPOINT")

    stt_manager = STTManager()
    tts_manager = TTSManager()
    llm_manager = LLMManager(OLLAMA_URL, LLM_CHECKPOINT)
    
    await llm_manager.start_session()

    stream_task = asyncio.create_task(process_queue(websocket, queue, stt_manager, llm_manager, tts_manager))

    try:
        stt_manager.audio_chunk_0 = await websocket.receive_bytes()
        while True:
            audio_chunk = await websocket.receive_bytes()
            await queue.put(audio_chunk)
    finally:
        stream_task.cancel()
        await llm_manager.close()
        await websocket.close()

