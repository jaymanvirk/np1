import asyncio
import time
import json
from ld_utils import get_detected_langs

async def stream_audio(websocket, text: str, tts_manager):
    dl = get_detected_langs(text)
    current = dl.head
    while current:
        audio_bytes = await tts_manager.get_output(text[current.start_index: current.end_index], current.lang)
        await websocket.send_bytes(audio_bytes)
        current = current.next

async def stream_output(websocket, stt_manager, llm_manager, tts_manager):
    m_id = int(time.time())
    text = ""
    incomplete_sentence = ""
    agen = llm_manager.chat(stt_manager.transcription)
    output = await anext(agen)
    if "§" not in output:
        text = output
        incomplete_sentence = output
        async for output in agen:
            tmp = incomplete_sentence + output + " "
            sentences = list(filter(None, tmp.split("±"))) 
            lns = len(sentences)
            if lns:
                if lns>1:
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

    if text:
        async with stt_manager.lock:
            stt_manager.id += 1
            stt_manager.audio_bytes = b''

