# Speech-to-text, Text response generation, Text-to-speech, Reverse image search

Plan:
1. STT
    1. send audio data from JS to FastAPI
    2. process audo for whisper turbo
    3. whisper large-v3-turbo
2. AWS EC2
    1. g4dn.xlarge
    2. nginx
    3. access via public ip
    4. route 53
3. Text response generation
    1. llama3.2:1B
    2. ollama
4. Text-to-speech
    1. OpenVoice
    2. StyleTTS
5. RIS
    1. Milvus DB
    2. Towhee
    3. Select open-source image feature extraction model
    5. Output top k similar photos
    6. Run similar photos through LLM

TODO:
1. Switch MongoDB to Cassandra

