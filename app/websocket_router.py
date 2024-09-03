from fastapi import WebSocket, WebSocketDisconnect, APIRouter
from get_transcription import get_transcription
import io
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
    buffer = []
    try:
        while True:
            data = await websocket.receive_bytes()
            audio_chunk = np.frombuffer(data, dtype=np.float32)
            buffer.extend(audio_chunk)
            
            # Process when buffer reaches a certain size
            if len(buffer) >= 16000:  # Process every 1 second of audio (assuming 16kHz sample rate)
                audio_data = np.array(buffer[:16000])
                buffer = buffer[16000:]
                
                # Transcribe the audio chunk
                segments, _ = get_transcription(audio_data)
                transcription = " ".join([segment.text for segment in segments])
                
                if transcription.strip():
                    await websocket.send_text(transcription)

            # audio_data = io.BytesIO(message)

            # try:
            #     segments, info = get_transcription(audio_data)
            #     await websocket.send_text(f"3. completed get_transcription: {list(segments)}")
            #     # for segment in segments:
            #     #     await websocket.send_text(f"{segment.start}, {segment.end}, {segment.text}")
            # except Exception as e:
            #     await websocket.send_text(f"3. Error get_transcription: {e}")
            #     break
            # finally:
            #     audio_data.close()

    except Exception as e:
        await websocket.send_text(f"Error: {e}")
    finally:
        await websocket.close()









