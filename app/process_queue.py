from get_processed_audio import get_processed_audio
from get_transcription import get_transcription
from send_generated_speech import send_generated_speech


async def process_queue(websocket
                        , queue
                        , audio_state):
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
                    await send_generated_speech(transcription, "female voice", websocket)
                else:
                   audio_state.prev_transcription = transcription
                t = time.time() - st

                await websocket.send_text(f"time: {t:.3f} | length: {ln} | {transcription}")


