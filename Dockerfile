# Use the official Python image from the Docker Hub
FROM python:3.12

RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy content into the container
COPY ./app /app
COPY ./static /app/static
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "-1", "--ws-ping-interval", "100", "--ws-ping-timeout", "100"]
