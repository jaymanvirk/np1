import asyncio 
import torch


VAD_MODEL, VAD_UTILS = torch.hub.load(repo_or_dir='snakers4/silero-vad', model='silero_vad', onnx=True)
# Optimize for CPU inference
torch.set_num_threads(1)
torch.set_num_interop_threads(1)

CHUNK_SIZE = 512
BATCH_SIZE = 10

async def is_speech(processed_audio, threshold=0.5, sampling_rate=16000):
    if len(processed_audio) % CHUNK_SIZE != 0:
        pad_length = CHUNK_SIZE - (len(processed_audio) % CHUNK_SIZE)
        processed_audio = np.pad(processed_audio, (0, pad_length), 'constant')
    
    num_chunks = len(processed_audio) // CHUNK_SIZE
    chunks = processed_audio[:num_chunks * CHUNK_SIZE].reshape(num_chunks, CHUNK_SIZE)

    for i in range(0, num_chunks, BATCH_SIZE):
        # Process a batch of chunks
        batch = chunks[i:i + BATCH_SIZE]
        batch_tensor = torch.from_numpy(batch).float()

        # Perform vectorized inference for the batch
        speech_probs = await asyncio.to_thread(lambda: VAD_MODEL(batch_tensor, sampling_rate))

        # Check if any chunk in the batch meets the condition
        if (speech_probs > threshold).any().item():
            return True
    
    return False 
