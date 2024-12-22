from audio_utils import get_processed_audio
from stt_utils import get_transcription 
from llm_utils import stream_llm_output
from vad_utils import is_speech
import os
import json
import asyncio


LLM_CHECKPOINT = os.getenv("LLM_CHECKPOINT")


async def process_queue(websocket
                        , queue
                        , stt_manager):
    strm = None
    while True:
        audio_chunk = await queue.get()
       
        tmp_chunk = await get_processed_audio(stt_manager.audio_chunk_0, audio_chunk)
        speech = await is_speech(tmp_chunk)

        if speech:
            if strm is not None and not strm.done() and stt_manager.sent_to_llm:
                strm.cancel()

            # Ensure exclusive access to shared state
            async with stt_manager.lock:
                stt_manager.sent_to_llm = False
                stt_manager.audio_bytes += audio_chunk
        
                audio_data = await get_processed_audio(stt_manager.audio_chunk_0, stt_manager.audio_bytes)

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
        elif not stt_manager.sent_to_llm:
            async with stt_manager.lock:
                stt_manager.sent_to_llm = True
            strm = asyncio.create_task(stream_llm_output(websocket, LLM_CHECKPOINT, stt_manager))
   
