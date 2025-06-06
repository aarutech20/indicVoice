# Use NVIDIA CUDA base image for GPU support
FROM nvidia/cuda:11.8-devel-ubuntu20.04

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.9 \
    python3.9-dev \
    python3-pip \
    python3.9-venv \
    git \
    wget \
    curl \
    build-essential \
    cmake \
    pkg-config \
    libsndfile1 \
    ffmpeg \
    sox \
    libsox-fmt-all \
    redis-server \
    && rm -rf /var/lib/apt/lists/*

# Create and set working directory
WORKDIR /app

# Create virtual environment
RUN python3.9 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Upgrade pip
RUN pip install --upgrade pip setuptools wheel

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install PyTorch with CUDA support
RUN pip install torch==2.0.1+cu118 torchaudio==2.0.2+cu118 --index-url https://download.pytorch.org/whl/cu118

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /app/staticfiles /app/media /app/logs

# Set permissions
RUN chmod +x manage.py

# Collect static files
RUN python manage.py collectstatic --noinput || true

# Create startup script
RUN echo '#!/bin/bash\n\
set -e\n\
\n\
# Start Redis in background\n\
redis-server --daemonize yes\n\
\n\
# Wait for Redis to start\n\
sleep 2\n\
\n\
# Run Django migrations\n\
python manage.py migrate --noinput\n\
\n\
# Create superuser if it does not exist\n\
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='\''admin'\'').exists() or User.objects.create_superuser('\''admin'\'', '\''admin@dubsync.com'\'', '\''admin123'\'')" || true\n\
\n\
# Start the application\n\
if [ "$1" = "dev" ]; then\n\
    echo "Starting development server..."\n\
    python manage.py runserver 0.0.0.0:8000\n\
else\n\
    echo "Starting production server..."\n\
    daphne -b 0.0.0.0 -p 8000 dubsync_backend.asgi:application\n\
fi' > /app/start.sh

RUN chmod +x /app/start.sh

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/health/ || exit 1

# Start the application
CMD ["/app/start.sh"]