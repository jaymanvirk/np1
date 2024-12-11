# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Install ffmpeg and clean up
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg git curl && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Download whisper module
RUN pip install --upgrade pip && \
    pip install git+https://github.com/openai/whisper.git

# Create a directory for model checkpoints
RUN mkdir -p /app/model_checkpoints

# Download the Whisper Turbo model
RUN python -c "import whisper; \
    model = whisper.load_model('tiny', download_root='/app/model_checkpoints/whisper');"

# Copy requirements.txt first to leverage caching
COPY requirements.txt .

# Install ollama
# RUN curl -sSL https://ollama.com/install.sh | sh


# Use a cache mount for pip installations
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt

# Now copy the application code and static files
COPY ./app /app
COPY ./static /app/static

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "-1", "--ws-ping-interval", "100", "--ws-ping-timeout", "100"]

