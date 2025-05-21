FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements files
COPY backend/requirements.txt backend-requirements.txt
COPY frontend/requirements.txt frontend-requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r backend-requirements.txt -r frontend-requirements.txt

# Copy the application code
COPY . .

# Set environment variables
ENV PYTHONPATH=/app
ENV PORT=8501

# Expose the port
EXPOSE 8501

# Start both services using a shell script
COPY start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"] 