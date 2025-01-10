import asyncio
import time
import json
from lingua import Language, LanguageDetectorBuilder
import os

LINGUA_LANGUAGES = os.getenv('LINGUA_LANGUAGES').split(',')
LANGUAGES = [getattr(Language, lang.strip().upper()) for lang in LINGUA_LANGUAGES]
DETECTOR = LanguageDetectorBuilder.from_languages(*LANGUAGES).build()

async def stream_audio(websocket, text: str, tts_manager):
    result = DETECTOR.detect_multiple_languages_of(text)
    for r in result:
        audio_bytes = await tts_manager.get_output(text[r.start_index: r.end_index], r.language.name.lower())
        await websocket.send_bytes(audio_bytes)

async def stream_output(websocket, stt_manager, llm_manager, tts_manager):
    m_id = int(time.time())
    text = ""
    incomplete_sentence = ""
    agen = llm_manager.get_chat(stt_manager.transcription)
    output = await anext(agen)
    if "§" not in output:
        async with stt_manager.lock:
            stt_manager.id += 1
            stt_manager.audio_bytes = b''
        text = output
        incomplete_sentence = output
        async for output in agen:
            tmp = incomplete_sentence + output + " "
            if "±" in tmp:
                sentences = list(filter(lambda x: x.strip(), tmp.split("±"))) 
                if len(sentences)>1:
                    incomplete_sentence = sentences[-1]
                    await stream_audio(websocket, sentences[0], tts_manager)
            else:
                incomplete_sentence += output + " "
            text += output
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

        if incomplete_sentence:
            await stream_audio(websocket, incomplete_sentence, tts_manager)


