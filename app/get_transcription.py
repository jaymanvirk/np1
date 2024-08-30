from faster_whisper import WhisperModel

def get_transcription(audio_data_float):
    model_size = "tiny.en"
    device = "cpu"
    compute_type = "int8"
    beam_size = 1
    
    # # Run on GPU with FP16
    # model = WhisperModel(model_size, device="cuda", compute_type="float16")
    # # or run on GPU with INT8
    # model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")
    # or run on CPU with INT8
    model = WhisperModel(model_size, device=device, compute_type=compute_type)
    
    return model.transcribe("test.m4a", beam_size=beam_size)