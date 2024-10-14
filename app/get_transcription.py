import whisper
import os


model_checkpoint = os.getenv("WHISPER_MODEL_CHECKPOINT")
device = os.getenv("WHISPER_DEVICE")
model = whisper.load_model(model_checkpoint).to(device) 

async def get_transcription(byte_stream) -> str:
    audio = whisper.load_audio(byte_stream)
    audio = whisper.pad_or_trim(audio)

    result = model.transcribe(audio)

    return result["text"]
