import whisper
import os
import torch

STT_CHECKPOINT = os.getenv("STT_CHECKPOINT")
GPU_DEVICE = os.getenv("GPU_DEVICE")
STT_MODEL = whisper.load_model(STT_CHECKPOINT).to(GPU_DEVICE)
STT_MODEL = torch.jit.script(STT_MODEL)

async def get_transcription(audio_data) -> str:
    with torch.no_grad():
        result = STT_MODEL.transcribe(audio_data)
    
    return result["text"]

