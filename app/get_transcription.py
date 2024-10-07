from whisper
import io

model_name = os.getenv("WHISPER_MODEL_NAME")
device = os.getenv("WHISPER_DEVICE")
model = whisper.load_modell(model_name, device=device)

async def transcribe_audio(file_bytes: bytes) -> str:
    audio_file = io.BytesIO(file_bytes)

    audio = whisper.load_audio(audio_file)
    audio = whisper.pad_or_trim(audio)

    result = model.transcribe(audio)

    return result["text"]
