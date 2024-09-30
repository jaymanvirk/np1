# Speech-to-text, Text response generation, Text-to-speech, Reverse image search

Plan:
1. STT
    1. send audio data from JS to FastAPI
    2. process audo for faster-whisper
    3. faster-whisper
2. Text response generation
    1. llama-cpp-python
3. Text-to-speech
    1. OpenVoice
    2. StyleTTS
5. RIS
    1. Milvus DB
    2. Towhee
    3. Select open-source image feature extraction model
    5. Output top k similar photos
    6. Run similar photos through LLM

