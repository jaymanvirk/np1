import asyncio
from llm_manager import ollama_manager
from tts_manager import tts_manager
import time
import json
import re

async def stream_audio(websocket, text):
    audio_bytes = await tts_manager.get_output(text)
    await websocket.send_bytes(audio_bytes)

async def stream_llm_output(websocket, model_name: str, stt_manager):
    """Function to stream output from the Ollama subprocess."""
    m_id = int(time.time())
    flag = False
    text = ""
    sentence_end = re.compile(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|!)\s')
    incomplete_sentence = ""
    async for output in ollama_manager.chat(stt_manager.transcription):
        flag = True
        text += output
        message = {
            "sender": {
                "name": "K"
            },
            "meta": {
                "id": m_id
            },
            "media": {
                "text": text 
            }
        }
        tmp = incomplete_sentence + output + " "
        sentences = sentence_end.split(tmp)
        if len(sentences) > 1:
            incomplete_sentence = sentences[-1]
            await stream_audio(websocket, sentences[0])
        else:
            incomplete_sentence += output + " "

        await websocket.send_text(json.dumps(message))

    if incomplete_sentence:
        await stream_audio(websocket, incomplete_sentence)

    if flag:
        async with stt_manager.lock:
            stt_manager.id += 1
            stt_manager.audio_bytes = b''
