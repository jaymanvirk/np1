from fastapi import WebSocket, WebSocketDisconnect, APIRouter
from get_transcription import get_transcription
import numpy as np

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
    try:
        while True:
            message = await websocket.receive_bytes()

            # Convert the received audio data to a NumPy array
            audio_data = np.frombuffer(message, dtype=np.int16)  # Adjust dtype based on your audio format
            
            # Transcribe the audio data
            # Whisper expects audio data in float32 format and normalized between -1.0 and 1.0
            audio_data_float = audio_data.astype(np.float32) / 32768.0  # Normalize 16-bit PCM to float32
 
            # Transcribe the audio
            segments, _ = get_transcription(audio_data_float)
            
            for segment in segments:
                await websocket.send(segment.text)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await websocket.close()









