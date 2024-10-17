import io
import numpy as np
import soundfile as sf
import subprocess


async def get_processed_audio(audio_bytes, ms = 500):
    # Convert audio bytes to WAV format using ffmpeg
    input_buffer = io.BytesIO(audio_bytes)
    output_buffer = io.BytesIO()

    # Use ffmpeg to convert the input audio bytes to WAV
    process = subprocess.Popen(
        ['ffmpeg', '-i', 'pipe:0', '-f', 'wav', 'pipe:1'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # Write the input bytes to ffmpeg's stdin and read from stdout
    wav_data, _ = process.communicate(input=input_buffer.read())

    # Read audio bytes directly into a numpy array using soundfile
    audio_segment, sr = sf.read(io.BytesIO(wav_data))

    # Calculate the number of samples to trim (ms to seconds)
    trim_samples = int(ms * sr / 1000)

    # Trim the audio segment directly using NumPy slicing
    trimmed_audio = audio_segment[trim_samples:]

    # Resample to 16 kHz if necessary
    if sr != 16000:
        # Calculate the resampling factor
        resample_factor = 16000 / sr
        new_length = int(len(trimmed_audio) * resample_factor)
        trimmed_audio = np.interp(
            np.linspace(0.0, 1.0, new_length), 
            np.linspace(0.0, 1.0, len(trimmed_audio)), 
            trimmed_audio
        )

    return trimmed_audio.astype(np.float32)
