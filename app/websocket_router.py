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
            try:
                message = await websocket.receive_bytes()
                await websocket.send_text(f"1. completed websocket.receive_bytes: {len(message)}")
            except Exception as e:
                await websocket.send_text(f"1. Error receiving message: {e}")
                break

            while len(message) % 2 != 0:
                message += b'\x00'
                
            try:
                audio_data = np.frombuffer(message, dtype=np.int16)
                await websocket.send_text(f"2.completed np.frombuffer: {len(audio_data)}")
            except Exception as e:
                await websocket.send_text(f"2. Error np.frombuffer: {e}")
                break

            try:
                audio_data_float = audio_data.astype(np.float32) / 32768.0
                await websocket.send_text(f"3. completed audio_data.astype: {len(audio_data_float)}")
            except Exception as e:
                await websocket.send_text(f"3. Error audio_data.astype: {e}")
                break

            try:
                segments, info = get_transcription(audio_data_float)
                await websocket.send_text(f"4. completed get_transcription: {list(segments)}")
                for segment in segments:
                    await websocket.send_text(f"{segment.start}, {segment.end}, {segment.text}")
            except Exception as e:
                await websocket.send_text(f"4. Error get_transcription: {e}")
                break
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await websocket.close()









