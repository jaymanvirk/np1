from whisper


model_name = os.getenv("WHISPER_MODEL_NAME")
device = os.getenv("WHISPER_DEVICE")
model = whisper.load_modell(model_name, device=device)

async def get_transcription(byte_stream) -> str:
    audio = whisper.load_audio(byte_stream)
    audio = whisper.pad_or_trim(audio)

    result = model.transcribe(audio)

    return result["text"]
