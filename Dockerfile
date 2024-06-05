# Use the official Python image from the Docker Hub
FROM python:latest

# Set the working directory in the container
WORKDIR /app

# Copy content into the container
COPY ./app /app
COPY ./static /app/static
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache -r requirements.txt

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]