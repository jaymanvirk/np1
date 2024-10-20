from fastapi import WebSocket, WebSocketDisconnect, APIRouter
from process_queue import process_queue
from audio_state import AudioState
import asyncio


router = APIRouter()

@router.websocket("/v1/audio")
async def handle_stream_audio(websocket: WebSocket):
    await websocket.accept()
    queue = asyncio.Queue()
    audio_state = AudioState()
    asyncio.create_task(process_queue(websocket, queue, audio_state))

    try:
        audio_state.audio_chunk_0 = await websocket.receive_bytes()
        audio_state.combined_audio = audio_state.audio_chunk_0
        counter = 0
        while True:
            audio_chunk = await websocket.receive_bytes()
            counter += 1
            await queue.put((counter, audio_chunk))

    except Exception as e:
        await websocket.send_text(f"Error: {e}")

    finally:
        await websocket.send_text(f"closing websocket")
        await websocket.close()

@router.websocket("/v1/image")
async def handle_upload_image(websocket: WebSocket):
    await websocket.accept()
    n = await websocket.receive_text()
    n = int(float(n)) + 1
    image_data = b''
    while n:
        try:
            image_data += await websocket.receive_bytes()
            n -= 1
        except WebSocketDisconnect:
            break

    await websocket.send_text(f"Received {len(image_data)}")








