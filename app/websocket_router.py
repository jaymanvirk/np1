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

    # Start ollama as a background task to prevent blocking
    asyncio.create_task(ollama_manager.start_process(LLM_CHECKPOINT))

    stream_task = asyncio.create_task(process_queue(websocket, queue, stt_manager))

    try:
        stt_manager.audio_chunk_0 = await websocket.receive_bytes()
        stt_manager.combined_audio = stt_manager.audio_chunk_0
        while True:
            audio_chunk = await websocket.receive_bytes()
            await queue.put(audio_chunk)
    except Exception as e:
        print(f"Error handle_stream_audio: {e}")

    finally:
        stream_task.cancel()
        ollama_manager.stop_process(LLM_CHECKPOINT)
        await websocket.close()

