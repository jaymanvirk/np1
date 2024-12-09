import asyncio 
import torch


VAD_MODEL, VAD_UTILS = torch.hub.load(repo_or_dir='snakers4/silero-vad', model='silero_vad', onnx=True)
MAX_AUDIO_LENGTH = 16000
# Optimize for CPU inference
VAD_MODEL.eval()
torch.set_num_threads(1)
torch.set_num_interop_threads(1)


async def is_speech(processed_audio, threshold=0.5, sampling_rate=16000):
    try:
        # Convert NumPy array to PyTorch tensor
        audio_tensor = torch.from_numpy(processed_audio).float()

        # Run VAD asynchronously
        speech_prob = await asyncio.to_thread(
            lambda: VAD_MODEL(audio_tensor, sampling_rate).item()
        )

        return speech_prob > threshold
    except Exception as e:
        return str(e)


