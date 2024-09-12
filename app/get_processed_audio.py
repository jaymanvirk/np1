def get_processed_audio(audio_bytes, ms = 100):
    audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes))
    audio_data = audio_segment[-ms:]
    byte_stream = io.BytesIO()
    audio_data.export(byte_stream, format="wav")
    byte_stream.seek(0)

    return byte_stream