import io
import numpy as np
import soundfile as sf
import asyncio 
import whisper
import os
import torch


VAD_MODEL, VAD_UTILS = torch.hub.load(repo_or_dir='snakers4/silero-vad', model='silero_vad', onnx=True)
MAX_AUDIO_LENGTH = 16000
AUDIO_TENSOR = torch.zeros(1, MAX_AUDIO_LENGTH, dtype=torch.float32)


STT_CHECKPOINT = os.getenv("STT_CHECKPOINT")
GPU_DEVICE = os.getenv("GPU_DEVICE")
STT_MODEL = whisper.load_model(STT_CHECKPOINT).to(GPU_DEVICE) 


async def get_transcription(audio_data) -> str:
    result = STT_MODEL.transcribe(audio_data)

    return result["text"]


async def is_speech(processed_audio, threshold=0.5, sampling_rate=16000):
    # Ensure audio is in the correct format and copy to pre-allocated tensor
    audio_length = min(len(processed_audio), MAX_AUDIO_LENGTH) 
    with torch.cuda.stream(torch.cuda.Stream()):
        AUDIO_TENSOR[0, :audio_length].copy_(torch.from_numpy(processed_audio[:audio_length]), non_blocking=True)
    
    # Run VAD asynchronously
    speech_prob = await asyncio.to_thread(lambda: VAD_MODEL(AUDIO_TENSOR[:, :audio_length], sampling_rate).item())
    
    return speech_prob > threshold


async def get_processed_audio(audio_bytes, ms = 500):
    # Convert audio bytes to WAV format using ffmpeg
    input_buffer = io.BytesIO(audio_bytes)
    output_buffer = io.BytesIO()

    # Use ffmpeg to convert the input audio bytes to WAV
    process = await asyncio.create_subprocess_exec(
        'ffmpeg', '-i', 'pipe:0', '-f', 'wav', 'pipe:1',
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    # Write the input bytes to ffmpeg's stdin and read from stdout
    wav_data, _ = await process.communicate(input=input_buffer.getvalue())

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
        trimmed_audio = await asyncio.to_thread(np.interp,
            np.linspace(0.0, 1.0, new_length),
            np.linspace(0.0, 1.0, len(trimmed_audio)),
            trimmed_audio
        )

    return trimmed_audio.astype(np.float32)

