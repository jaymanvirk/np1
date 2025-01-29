import asyncio


class STTManager:
    def __init__(self):
        self.audio_chunk_0 = b''
        self.audio_bytes = b''
        self.transcription = "Hi"
        # Lock for synchronizing access to shared state
        self.lock = asyncio.Lock()  
        self.sent_to_llm = True 
        self.id = 0

