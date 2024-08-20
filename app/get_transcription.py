from faster_whisper import WhisperModel


def get_transcription(audio_data_float):
    model_size = "base"

    # # Run on GPU with FP16
    # model = WhisperModel(model_size, device="cuda", compute_type="float16")
    # # or run on GPU with INT8
    # model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")
    # # or run on CPU with INT8
    model = WhisperModel(model_size, device="cpu", compute_type="int8")


    return model.transcribe(audio_data_float, beam_size=5)