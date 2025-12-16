# Read the doc: https://huggingface.co/docs/hub/spaces-sdks-docker
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application files
COPY . .

# Create data directory
RUN mkdir -p data

# Expose port 7860 (required by Hugging Face Spaces)
EXPOSE 7860

# Set environment variables
ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=1

# Run the application on port 7860
CMD ["python", "-u", "app.py"]
