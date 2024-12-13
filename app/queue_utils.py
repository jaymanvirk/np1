from audio_utils import get_processed_audio
from stt_utils import get_transcription
from llm_utils import stream_ollama_output
from vad_utils import is_speech
import os
import json


LLM_CHECKPOINT = os.getenv("LLM_CHECKPOINT")


async def process_queue(websocket
                        , queue
                        , stt_manager):
    while True:
        audio_chunk = await queue.get()
       
        tmp_chunk = await get_processed_audio(stt_manager.audio_chunk_0 + audio_chunk)
        speech = await is_speech(tmp_chunk)

        if speech:
            # Ensure exclusive access to shared state
            async with stt_manager.lock:  
                stt_manager.combined_audio += audio_chunk
        
                audio_data = await get_processed_audio(stt_manager.combined_audio)

                transcription = await get_transcription(audio_data)
                stt_manager.transcription = transcription
 
                message = {
                    "sender": {
                        "name": "Me"
                    },
                    "meta": {
                        "id": stt_manager.id
                    },
                    "media": {
                        "text": transcription
                    }
                }

            await websocket.send_text(json.dumps(message))
        elif len(stt_manager.transcription):
            await stream_ollama_output(websocket, LLM_CHECKPOINT, stt_manager.transcription)
   
