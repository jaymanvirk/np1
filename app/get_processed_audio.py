from pydub import AudioSegment
import io

def get_processed_audio(audio_bytes):
    audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes))
    indx = len(audio_segment)//2
    byte_stream = io.BytesIO()
    audio_segment[indx:].export(byte_stream, format="wav")
    byte_stream.seek(0)

    return byte_stream