from audio_utils import get_processed_audio
from transcription_utils import get_transcription
from llm_utils import is_thought_complete, stream_ollama_output


async def process_queue(websocket
                        , queue
                        , audio_state):
    while True:
        audio_chunk = await queue.get()
        # Ensure exclusive access to shared state
        async with audio_state.lock:  
            audio_state.combined_audio += audio_chunk

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

            transcription = transcription.replace("\"", "\\\"")
            json = f'
                    {{
                        "sender":
                            {{
                                "name":"You"
                            }}
                        , "media":
                            {{
                                "text": "{transcription}"
                            }}
                    }}
            '
            await websocket.send_text(json)
