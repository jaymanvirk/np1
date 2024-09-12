from faster_whisper import WhisperModel


model_size = "tiny"
device = "cuda"
compute_type = "int8"
beam_size = 5
model = WhisperModel(model_size, device=device, compute_type=compute_type)


async def get_transcription(audio_data):
    
    return model.transcribe(audio_data, beam_size=beam_size)