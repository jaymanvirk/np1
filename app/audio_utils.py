import io
import numpy as np
import soundfile as sf
import asyncio 


async def get_processed_audio(audio_chunk_0, audio_bytes):
    combined_audio = audio_chunk_0 + audio_bytes

    # Use ffmpeg to convert the input audio bytes to WAV
    process = await asyncio.create_subprocess_exec(
        'ffmpeg', '-i', 'pipe:0', '-ar', '16000', '-ac', '1', '-f', 'wav', 'pipe:1',
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    # Write the input bytes to ffmpeg's stdin and read from stdout
    wav_data, _ = await process.communicate(input=combined_audio)

    # Read audio bytes directly into a numpy array using soundfile
    audio_segment, sr = await asyncio.to_thread(sf.read, io.BytesIO(wav_data))

    # Calculate the number of samples to remove (length of audio_chunk_0)
    chunk_0_samples = int(len(audio_chunk_0) * sr / len(combined_audio))

    # Remove audio_chunk_0 from audio_segment
    trimmed_audio = audio_segment[chunk_0_samples:]

    # Resample to 16 kHz if necessary
    if sr != 16000:
        # Calculate the resampling factor
        resample_factor = 16000 / sr
        new_length = int(len(trimmed_audio) * resample_factor)
        trimmed_audio = await asyncio.to_thread(np.interp,
            np.linspace(0.0, 1.0, new_length),
            np.linspace(0.0, 1.0, len(trimmed_audio)),
            trimmed_audio
        )

    return trimmed_audio.astype(np.float32)


