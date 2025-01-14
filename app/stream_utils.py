import asyncio
import time
import json
from lingua import Language, LanguageDetectorBuilder
import os
from stt_utils import get_transcription 
from audio_utils import get_processed_audio


LINGUA_LANGUAGES = os.getenv('LINGUA_LANGUAGES').split(',')
LANGUAGES = [getattr(Language, lang.strip().upper()) for lang in LINGUA_LANGUAGES]
DETECTOR = LanguageDetectorBuilder.from_languages(*LANGUAGES).build()

async def stream_transcription(websocket, stt_manager):
    audio_data = await get_processed_audio(stt_manager.audio_chunk_0, stt_manager.audio_bytes)
    transcription = await get_transcription(audio_data)
    stt_manager.transcription = transcription

    message = {
        "type": "message"
        ,"sender": {
            "name": "Me"
        }
        ,"meta": {
            "id": stt_manager.id
        }
        ,"media": {
            "text": transcription
        }
    }

    await websocket.send_text(json.dumps(message))



async def stream_audio(websocket, text: str, tts_manager):
    """
    result = DETECTOR.detect_multiple_languages_of(text)
    logger.info("STREAM AUDIO:")
    logger.info(f'{text} | {result}')
    for r in result:
        audio_bytes = await tts_manager.get_output(text[r.start_index: r.end_index], r.language.name.lower())
        await websocket.send_bytes(audio_bytes)
    """
    audio_bytes = await tts_manager.get_output(text, "english")
    await websocket.send_bytes(audio_bytes)

async def stream_output(websocket, stt_manager, llm_manager, tts_manager):
    m_id = int(time.time())
    text = ""
    tmp = ""
    agen = llm_manager.get_chat(stt_manager.transcription)
    output = await anext(agen)
    if "§" not in output:
        async with stt_manager.lock:
            stt_manager.id += 1
            stt_manager.audio_bytes = b''
        text = output
        tmp = output
        async for output in agen:
            if "±" in tmp:
                sentences = list(filter(None, tmp.split("±")))
                tmp = ""
                if len(sentences)>1:
                    tmp = sentences[-1]
                await stream_audio(websocket, sentences[0], tts_manager)
            else:
                tmp += output
            text += output.replace("±","")
            message = {
                "type": "message"
                ,"sender": {
                    "name": "K"
                }
                ,"meta": {
                    "id": m_id
                }
                ,"media": {
                    "text": text
                }
            }
            asyncio.create_task(websocket.send_text(json.dumps(message)))

        if tmp:
            await stream_audio(websocket, tmp, tts_manager)


