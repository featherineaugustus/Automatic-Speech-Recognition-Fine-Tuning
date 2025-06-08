# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=asr/asr_api.py
ENV FLASK_ENV=development

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install dependencies
# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY asr /app/asr

# Expose the port the app runs on
EXPOSE 8001

# Run the Flask application
CMD ["flask", "run", "--host=0.0.0.0", "--port=8001"]