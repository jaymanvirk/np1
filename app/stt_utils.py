import whisper
import os
import torch

MC_DIR = os.getenv("MC_DIR")
STT_DIR = os.getenv("STT_DIR")
STT_CHECKPOINT = os.getenv("STT_CHECKPOINT")
GPU_DEVICE = os.getenv("GPU_DEVICE")
STT_MODEL = whisper.load_model(f'{MC_DIR}/{STT_DIR}/{STT_CHECKPOINT}').to(GPU_DEVICE)
STT_MODEL = torch.jit.script(STT_MODEL)

async def get_transcription(audio_data) -> str:
    with torch.no_grad():
        result = STT_MODEL.transcribe(audio_data)
    
    return result["text"]

