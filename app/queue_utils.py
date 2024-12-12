from audio_utils import get_processed_audio
from stt_utils import get_transcription
from llm_utils import stream_ollama_output
from vad_utils import is_speech
import os
import json


LLM_CHECKPOINT = os.getenv("LLM_CHECKPOINT")


async def process_queue(websocket
                        , queue
                        , audio_state):
    while True:
        audio_chunk = await queue.get()
       
        tmp_chunk = await get_processed_audio(audio_state.audio_chunk_0 + audio_chunk)
        speech = await is_speech(tmp_chunk)

        if speech:
            # Ensure exclusive access to shared state
            async with audio_state.lock:  
                audio_state.combined_audio += audio_chunk
        
                audio_data = await get_processed_audio(audio_state.combined_audio)

                transcription = await get_transcription(audio_data)
                audio_state.prev_transcription = transcription
 
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
        elif audio_state.combined_audio != audio_state.audio_chunk_0:
            await stream_ollama_output(websocket, LLM_CHECKPOINT, audio_state.prev_transcription)
   
