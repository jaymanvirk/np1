from fastapi import WebSocket, WebSocketDisconnect, APIRouter
from get_transcription import get_transcription
from get_processed_audio import get_processed_audio
import asyncio
import time


router = APIRouter()

class AudioState:
    def __init__(self):
        self.audio_chunk_0 = b''
        self.combined_audio = b''
        self.prev_transcription = ""
        # Lock for synchronizing access to shared state
        self.lock = asyncio.Lock()  

@router.websocket("/v1/audio")
async def handle_stream_audio(websocket: WebSocket):
    await websocket.accept()
    queue = asyncio.Queue()
    audio_state = AudioState()
    asyncio.create_task(process_queue(websocket, queue, audio_state))

    try:
        audio_state.audio_chunk_0 = await websocket.receive_bytes()
        audio_state.combined_audio = audio_state.audio_chunk_0

        while True:
            audio_chunk = await websocket.receive_bytes()
            await queue.put(audio_chunk)

    except Exception as e:
        await websocket.send_text(f"Error: {e}")

    finally:
        await websocket.send_text(f"closing websocket")
        await websocket.close()


async def process_queue(websocket: WebSocket
                        , queue: asyncio.Queue
                        , audio_state: AudioState):
    while True:
        st = time.time()
        audio_chunk = await queue.get()
        # Ensure exclusive access to shared state
        async with audio_state.lock:  
            audio_state.combined_audio += audio_chunk
            ln = len(audio_state.combined_audio)

        audio_data = await get_processed_audio(audio_state.combined_audio)

        transcription = await get_transcription(audio_data)
        # Lock again for state updates
        async with audio_state.lock:  
            if transcription:
                if audio_state.prev_transcription == transcription:
                    audio_state.combined_audio = audio_state.audio_chunk_0 + audio_chunk
                else:
                   audio_state.prev_transcription = transcription
                t = time.time() - st

                await websocket.send_text(f"time: {t:.3f} | length: {ln} | {transcription}")


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








