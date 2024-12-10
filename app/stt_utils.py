import whisper
import os


STT_CHECKPOINT = os.getenv("STT_CHECKPOINT")
GPU_DEVICE = os.getenv("GPU_DEVICE")
STT_MODEL = whisper.load_model(STT_CHECKPOINT).to(GPU_DEVICE) 


async def get_transcription(audio_data) -> str:
    result = STT_MODEL.transcribe(audio_data)

    return result["text"]

