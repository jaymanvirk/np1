from fastapi import WebSocket, WebSocketDisconnect, APIRouter
from get_transcription import get_transcription
from get_processed_audio import get_processed_audio
# import asyncio
# from concurrent.futures import ThreadPoolExecutor
import time
import io

router = APIRouter()

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


@router.websocket("/v1/audio")
async def handle_stream_audio(websocket: WebSocket):
    await websocket.accept()
    pt = ''

    try:
        audio_chunk_0 = await websocket.receive_bytes()
        combined_audio = audio_chunk_0

        while True:
            st = time.time()
            audio_chunk = await websocket.receive_bytes()
            combined_audio += audio_chunk
            ln = len(combined_audio)

            byte_stream = await get_processed_audio(combined_audio)
            # byte_stream = await asyncio.get_event_loop().run_in_executor(executor, lambda: io.BytesIO(combined_audio))
            
            segments, _ = await get_transcription(byte_stream)

            transcription = " ".join([segment.text for segment in segments]).strip()
            
            if transcription:
                if pt == transcription:
                    # TODO: 
                    # run a model "if the thought complete?"
                    # if yes, send to a bigger model

                    combined_audio = audio_chunk_0 + audio_chunk
                else:
                    pt = transcription
                t = time.time() - st
                await websocket.send_text(f'time: {t:.3f} | length: {ln} | {transcription}')

            



    except Exception as e:
        await websocket.send_text(f"Error: {e}")
    finally:
        await websocket.send_text(f"closing websocket")
        await websocket.close()







