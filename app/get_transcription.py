import whisper
import os


model_checkpoint = os.getenv("WHISPER_MODEL_CHECKPOINT")
device = os.getenv("WHISPER_DEVICE")
model = whisper.load_model(model_checkpoint).to(device) 

async def get_transcription(audio_data) -> str:
    result = model.transcribe(audio_data)

    return result["text"]
