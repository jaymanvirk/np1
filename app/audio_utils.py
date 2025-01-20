import io
import numpy as np
import soundfile as sf
import asyncio 


async def get_processed_audio(audio_chunk_0, audio_chunk):
    combined_audio = audio_chunk_0 + audio_chunk
    process = await asyncio.create_subprocess_exec(
        'ffmpeg', '-i', 'pipe:0', '-f', 'wav', 'pipe:1',
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    wav_data, _ = await process.communicate(input=combined_audio)

    audio_segment, sr = await asyncio.to_thread(sf.read, io.BytesIO(wav_data))

    chunk_0_samples = int(len(audio_chunk_0) * len(audio_segment) / len(combined_audio))

    trimmed_audio = audio_segment[chunk_0_samples:]

    if sr != 16000:
        resample_factor = 16000 / sr
        new_length = int(len(trimmed_audio) * resample_factor)
        trimmed_audio = await asyncio.to_thread(np.interp,
            np.linspace(0.0, 1.0, new_length),
            np.linspace(0.0, 1.0, len(trimmed_audio)),
            trimmed_audio
        )

    return trimmed_audio.astype(np.float32)


