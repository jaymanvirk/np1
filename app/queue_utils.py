from stt_utils import get_transcription, get_processed_audio, is_speech
from llm_utils import is_thought_complete, stream_ollama_output
import os
import json


LLM_CHECKPOINT = os.getenv("LLM_CHECKPOINT")


async def process_queue(websocket
                        , queue
                        , audio_state):
    while True:
        audio_chunk = await queue.get()
       
        tmp_chunk = await get_processed_audio(audio_chunk)
        speech = await is_speech(tmp_chunk)

        if speech:
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
                        thought_complete = await is_thought_complete(LLM_CHECKPOINT, transcription)
                        if bool(thought_complete):
                            audio_state.id += 1 
                            await stream_ollama_output(websocket, LLM_CHECKPOINT, transcription)
                    else:
                       audio_state.prev_transcription = transcription
                else:
                    audio_state.combined_audio = audio_state.audio_chunk_0
            
                message = {
                    "sender": {
                        "name": "Me"
                    },
                    "meta": {
                        "id": audio_state.id
                    },
                    "media": {
                        "text": transcription
                    }
                }

                await websocket.send_text(json.dumps(message))
