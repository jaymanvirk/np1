from fastapi import WebSocket, WebSocketDisconnect, APIRouter
from get_transcription import get_transcription
import io
import numpy as np
from pydub import AudioSegment

router = APIRouter()

@router.websocket("/upload/image")
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


@router.websocket("/stream/audio")
async def handle_stream_audio(websocket: WebSocket):
    await websocket.accept()
    audio_buffer = b''

    try:
        while True:
            audio_chunk = await websocket.receive_bytes()
            audio_buffer += audio_chunk
            audio_data = io.BytesIO(audio_buffer)

            # audio_array = np.frombuffer(audio_chunk, dtype=np.float32)

            # max_val = np.max(np.abs(audio_array))
            # if max_val > 0:
            #     audio_array_norm = audio_array / max_val
            # else:
            #     audio_array_norm = audio_array
 
            segments, _ = await get_transcription(audio_data)
            transcription = " ".join([segment.text for segment in segments])

            if transcription.strip():
                await websocket.send_text(transcription)


    except Exception as e:
        await websocket.send_text(f"Error: {e}")
    finally:
        await websocket.close()









