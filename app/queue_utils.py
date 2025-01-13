from audio_utils import get_processed_audio
from stream_utils import stream_output, stream_transcription
from vad_utils import is_speech
import json
import asyncio


async def process_queue(websocket
                        , queue
                        , stt_manager
                        , llm_manager
                        , tts_manager):
    tasks_llm = []
    tasks_stt = []
    while True:
        audio_chunk = await queue.get()
       
        tmp_chunk = await get_processed_audio(stt_manager.audio_chunk_0, audio_chunk)
        speech = await is_speech(tmp_chunk)

        if speech:
            if stt_manager.sent_to_llm:
                for t in tasks_llm:
                    t.cancel()

                message = {
                    "type": "command" 
                    ,"command": "stop_audio" 
                }

                await websocket.send_text(json.dumps(message))

                await asyncio.gather(*tasks_llm, return_exceptions=True)
                tasks_llm.clear()

            async with stt_manager.lock:
                stt_manager.sent_to_llm = False
                stt_manager.audio_bytes += audio_chunk
            diff = len(stt_manager.audio_bytes) - (len(tasks_stt)+1)*8000
            if diff > -1:
                tasks_stt.append(asyncio.create_task(stream_transcription(websocket, stt_manager)))
        elif not stt_manager.sent_to_llm:
            async with stt_manager.lock:
                stt_manager.sent_to_llm = True
            for t in tasks_stt:
                t.cancel()
            await asyncio.gather(*tasks_stt, return_exceptions=True)
            tasks_stt.clear()
            if diff < 0:
                await stream_transcription(websocket, stt_manager)
            tasks_llm.append(asyncio.create_task(stream_output(websocket, stt_manager, llm_manager, tts_manager)))


