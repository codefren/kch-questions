FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy start script and make it executable
COPY start.sh .
RUN chmod +x start.sh

# Copy rest of application code
COPY . .

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["bash", "./start.sh"]
