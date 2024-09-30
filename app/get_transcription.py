from faster_whisper import WhisperModel
import os

model_size = os.getenv("WHISPER_MODEL_SIZE")
device = os.getenv("WHISPER_DEVICE")
compute_type = os.getenv("WHISPER_COMPUTE_TYPE")
beam_size = int(os.getenv("WHISPER_BEAM_SIZE"))
model = WhisperModel(model_size, device=device, compute_type=compute_type)


async def get_transcription(audio_data):
    
    return model.transcribe(audio_data, beam_size=beam_size)