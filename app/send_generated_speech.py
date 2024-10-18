import torch
from parler_tts import ParlerTTSForConditionalGeneration, ParlerTTSStreamer
from transformers import AutoTokenizer

torch_device = "cuda"
torch_dtype = torch.bfloat16
model_name = "parler-tts/parler-tts-mini-v1"

# Load model and tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = ParlerTTSForConditionalGeneration.from_pretrained(model_name).to(torch_device, dtype=torch_dtype)

sampling_rate = model.audio_encoder.config.sampling_rate
frame_rate = model.audio_encoder.config.frame_rate


async def send_generated_speech(text, description, websocket, play_steps_in_s=0.5):
    play_steps = int(frame_rate * play_steps_in_s)
    streamer = ParlerTTSStreamer(model, device=torch_device, play_steps=play_steps)

    # Tokenization
    inputs = tokenizer(description, return_tensors="pt").to(torch_device)
    prompt = tokenizer(text, return_tensors="pt").to(torch_device)

    # Create generation kwargs
    generation_kwargs = {
        "input_ids": inputs.input_ids,
        "prompt_input_ids": prompt.input_ids,
        "attention_mask": inputs.attention_mask,
        "prompt_attention_mask": prompt.attention_mask,
        "streamer": streamer,
        "do_sample": True,
        "temperature": 1.0,
        "min_new_tokens": 10,
    }

    # Generate audio asynchronously
    await model.generate(**generation_kwargs)

    # Iterate over chunks of audio and send via WebSocket
    async for new_audio in streamer:
        if new_audio.shape[0] == 0:
            break
        await websocket.send_bytes(new_audio.cpu().numpy().tobytes())

