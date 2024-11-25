from audio_utils import get_processed_audio
from transcription_utils import get_transcription
from llm_utils import is_thought_complete, stream_ollama_output
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
                    thought_complete = await is_thought_complete("llama3.2:3b", transcription)
                    if bool(thought_complete):
                        await stream_ollama_output(websocket, "llama3.2:3b", transcription)
                else:
                   audio_state.prev_transcription = transcription
            else:
                audio_state.combined_audio = audio_state.audio_chunk_0

            t = time.time() - st
            await websocket.send_text(f'{{"sender":{{"name":"You"}}, "media":{{"text": "chunk: {counter} | time: {t:.3f} | length: {ln} | {transcription.replace("\"", "\\\"")}"}}}}')
            
