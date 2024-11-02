from audio_utils import get_processed_audio
from transcription_utils import get_transcription
import time


async def process_queue(websocket
                        , queue
                        , audio_state):
    while True:
        st = time.time()
        counter, audio_chunk = await queue.get()
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
                    transcription = "thought complete?"
                else:
                   audio_state.prev_transcription = transcription
            else:
                audio_state.combined_audio = audio_state.audio_chunk_0
                transcription = "silence"

            t = time.time() - st
            await websocket.send_text(f'{{"sender":{{"name":"You"}}, "media":{{"text": "chunk: {counter} | time: {t:.3f} | length: {ln} | {transcription.replace("\"", "\\\"")}"}}}}')
            
