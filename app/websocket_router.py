from fastapi import WebSocket, APIRouter
from queue_utils import process_queue
from stt_manager import AudioState
from llm_manager import ollama_manager
import asyncio
import os


LLM_CHECKPOINT = os.getenv("LLM_CHECKPOINT")

router = APIRouter()

@router.websocket("/v1/audio")
async def handle_stream_audio(websocket: WebSocket):
    await websocket.accept()
    queue = asyncio.Queue()
    audio_state = AudioState()
    stream_task = asyncio.create_task(process_queue(websocket, queue, audio_state))

    try:
        audio_state.audio_chunk_0 = await websocket.receive_bytes()
        audio_state.combined_audio = audio_state.audio_chunk_0
        while True:
            audio_chunk = await websocket.receive_bytes()
            await queue.put(audio_chunk)
    except websockets.exceptions.ConnectionClosed:
        print("WebSocket connection closed")
    except Exception as e:
        print(f"Error handle_stream_audio: {e}")

    finally:
        stream_task.cancel()
        ollama_manager.stop_process(LLM_CHECKPOINT)
        await websocket.close()

