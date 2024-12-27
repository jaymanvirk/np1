import asyncio
from tts_manager import TTSManager 
import time
import json
import os
import re


TTS_CHECKPOINT = os.getenv("TTS_CHECKPOINT")


async def stream_audio(websocket, text):
    tts_manager = TTSManager(TTS_CHECKPOINT)
    audio_bytes = await tts_manager.get_output(text)
    await websocket.send_bytes(audio_bytes)


async def stream_output(websocket, model_name: str, stt_manager, llm_manager):
    """Function to stream output from the Ollama subprocess."""
    m_id = int(time.time())
    text = ""
    incomplete_sentence = ""
    sentence_endings = r'(?<=[.!?])(?:\s+)?(?=[A-Z])'
    agen = llm_manager.chat(stt_manager.transcription)
    output = await anext(agen)
    if "§" not in output:
        text = output
        incomplete_sentence = output
        async for output in agen:
            tmp = incomplete_sentence + output + " "
            sentences = re.split(sentence_endings, tmp)
            if len(sentences) > 1:
                incomplete_sentence = sentences[-1]
                await stream_audio(websocket, sentences[0])
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
            await stream_audio(websocket, incomplete_sentence)

    if text:
        async with stt_manager.lock:
            stt_manager.id += 1
            stt_manager.audio_bytes = b''

