import asyncio


class STTManager:
    def __init__(self):
        self.audio_chunk_0 = b''
        self.combined_audio = b''
        self.transcription = ""
        # Lock for synchronizing access to shared state
        self.lock = asyncio.Lock()  
        self.id = 0
