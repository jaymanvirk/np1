import asyncio


class AudioState:
    def __init__(self):
        self.audio_chunk_0 = b''
        self.combined_audio = b''
        self.prev_transcription = ""
        # Lock for synchronizing access to shared state
        self.lock = asyncio.Lock()  
        self._id = -1 

    async def get_next_id(self):
        async with self.lock:
            self._id += 1
            return self._id
