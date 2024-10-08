import whisper
import os


model_path = os.getenv("WHISPER_MODEL_PATH")
device = os.getenv("WHISPER_DEVICE")
model = whisper.load_model(model_path, device=device)

async def get_transcription(byte_stream) -> str:
    audio = whisper.load_audio(byte_stream)
    audio = whisper.pad_or_trim(audio)

    result = model.transcribe(audio)

    return result["text"]
