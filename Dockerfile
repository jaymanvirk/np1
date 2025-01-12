# Use the official Python image from the Docker Hub
FROM python:3.12-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    ffmpeg \
    git \
    curl \
    build-essential \
    espeak-ng \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Download whisper module
RUN pip install --upgrade pip && \
    pip install git+https://github.com/openai/whisper.git && \
    pip install torchaudio onnxruntime

# Create a directory for model checkpoints
RUN mkdir -p /app/model_checkpoints

# Download the Whisper Turbo model
RUN python -c "import whisper; \
    model = whisper.load_model('turbo', download_root='/app/model_checkpoints/whisper');"

RUN python -c "import torch; \
    model = torch.hub.load(repo_or_dir='snakers4/silero-vad', model='silero_vad', onnx=True);"

# Install piper-tts
COPY install_pipertts.sh .
RUN chmod +x ./install_pipertts.sh \
    && ./install_pipertts.sh

# Install ollama
RUN curl -sSL https://ollama.com/install.sh | sh

COPY Modelfile .

RUN ollama serve & \
    sleep 5 && \
    ollama create k -f ./Modelfile && \
    ollama pull mxbai-embed-large

# Copy requirements.txt first to leverage caching
COPY requirements.txt .

# Use a cache mount for pip installations
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt

# Now copy the application code and static files
COPY ./app /app
COPY ./static /app/static

# Command to run the application
COPY startup.sh .
RUN chmod +x ./startup.sh
CMD ["./startup.sh"]
