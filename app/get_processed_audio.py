from pydub import AudioSegment
import io

async def get_processed_audio(audio_bytes, ms = 500):
    audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes))
    byte_stream = io.BytesIO()
    audio_segment[ms:].export(byte_stream, format="wav")
    byte_stream.seek(0)

    return byte_stream