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
            print("ENTERED THE LOOP")
            try:
                message = await websocket.receive_bytes()
                print(len(message))
            except Exception as e:
                print(f"Error receiving message: {e}")
                break
                
            # try:
            #     audio_data = np.frombuffer(message, dtype=np.int16)
            # except Exception as e:
            #     print(f"Error np.frombuffer: {e}")
            #     break

            # try:
            #     audio_data_float = audio_data.astype(np.float32) / 32768.0
            # except Exception as e:
            #     print(f"Error .astype: {e}")
            #     break

            # try:
            #     segments, _ = get_transcription(audio_data_float)
            #     for segment in segments:
            #         await websocket.send_text(segment.text)
            # except Exception as e:
            #     print(f"Error get_transcription: {e}")
            #     break
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await websocket.close()









