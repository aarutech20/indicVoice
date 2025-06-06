# 🚀 DubSync Deployment Guide

This guide provides step-by-step instructions for deploying DubSync in various environments.

## 📋 Prerequisites

### System Requirements
- **OS**: Linux (Ubuntu 20.04+), macOS, or Windows with WSL2
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 10GB free space for models and dependencies
- **GPU**: NVIDIA GPU with 4GB+ VRAM (optional, CPU fallback available)

### Software Requirements
- **Docker**: 20.10+ with Docker Compose
- **Git**: For cloning the repository
- **NVIDIA Docker** (for GPU support): nvidia-docker2

## 🐳 Docker Deployment (Recommended)

### 1. Quick Start
```bash
# Clone the repository
git clone https://github.com/ARAVINDAN20/DubSync---Real-Time-Speech-Transcription.git
cd DubSync---Real-Time-Speech-Transcription

# Run automated setup
chmod +x scripts/setup.sh
./scripts/setup.sh
```

### 2. Manual Docker Setup

#### For GPU Systems
```bash
# Build and start services
docker-compose up --build -d

# View logs
docker-compose logs -f

# Access application
# Frontend: http://localhost:3000
# Backend: http://localhost:8000/api
# Admin: http://localhost:8000/admin (admin/admin123)
```

#### For CPU-Only Systems
```bash
# Use CPU-specific configuration
docker-compose -f docker-compose.cpu.yml up --build -d

# Monitor startup (may take longer for model loading)
docker-compose -f docker-compose.cpu.yml logs -f backend
```

### 3. Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit configuration
nano .env

# Key settings:
# SECRET_KEY=your-secret-key-here
# DEBUG=False  # For production
# CUDA_VISIBLE_DEVICES=0  # GPU device ID
```

## 💻 Local Development Setup

### Backend Setup
```bash
cd backend

# Create virtual environment
python3.9 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start Redis (required for WebSocket)
redis-server

# Start Django server
python manage.py runserver 0.0.0.0:8000
```

### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Access: http://localhost:3000
```

## ☁️ Cloud Deployment

### AWS EC2 Deployment

#### 1. Launch EC2 Instance
```bash
# Recommended instance types:
# GPU: p3.2xlarge, g4dn.xlarge
# CPU: c5.2xlarge, m5.2xlarge

# Security groups:
# Port 22 (SSH)
# Port 80 (HTTP)
# Port 443 (HTTPS)
# Port 3000 (Frontend)
# Port 8000 (Backend)
```

#### 2. Setup Instance
```bash
# Connect to instance
ssh -i your-key.pem ubuntu@your-instance-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# For GPU instances, install NVIDIA Docker
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get update && sudo apt-get install -y nvidia-docker2
sudo systemctl restart docker
```

#### 3. Deploy Application
```bash
# Clone repository
git clone https://github.com/ARAVINDAN20/DubSync---Real-Time-Speech-Transcription.git
cd DubSync---Real-Time-Speech-Transcription

# Configure for production
cp .env.example .env
nano .env  # Set production values

# Deploy
docker-compose up --build -d

# Setup SSL (optional)
sudo apt install certbot
sudo certbot --nginx -d your-domain.com
```

### Google Cloud Platform

#### 1. Create VM Instance
```bash
# Using gcloud CLI
gcloud compute instances create dubsync-vm \
    --zone=us-central1-a \
    --machine-type=n1-standard-4 \
    --accelerator=type=nvidia-tesla-t4,count=1 \
    --image-family=ubuntu-2004-lts \
    --image-project=ubuntu-os-cloud \
    --boot-disk-size=50GB \
    --maintenance-policy=TERMINATE \
    --restart-on-failure
```

#### 2. Setup and Deploy
```bash
# SSH to instance
gcloud compute ssh dubsync-vm --zone=us-central1-a

# Follow same setup steps as AWS
# Install Docker, NVIDIA Docker, clone repo, deploy
```

## 🔧 Production Configuration

### Environment Variables
```bash
# Backend (.env)
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com,localhost
DATABASE_URL=postgresql://user:pass@host:5432/dbname
REDIS_URL=redis://redis:6379/0
CUDA_VISIBLE_DEVICES=0

# Frontend
VITE_API_BASE_URL=https://your-domain.com/api
```

### Nginx Configuration
```nginx
# /etc/nginx/sites-available/dubsync
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /ws/ {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### SSL Setup
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

## 📊 Monitoring & Maintenance

### Health Checks
```bash
# Check service status
docker-compose ps

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Health endpoints
curl http://localhost:8000/api/health/
curl http://localhost:3000/
```

### Performance Monitoring
```bash
# System resources
htop
nvidia-smi  # For GPU usage

# Docker stats
docker stats

# Application metrics
# Backend: http://localhost:8000/admin/
# Logs: docker-compose logs
```

### Backup & Recovery
```bash
# Backup database
docker-compose exec backend python manage.py dumpdata > backup.json

# Backup volumes
docker run --rm -v dubsync_redis_data:/data -v $(pwd):/backup alpine tar czf /backup/redis_backup.tar.gz /data

# Restore
docker-compose exec backend python manage.py loaddata backup.json
```

## 🔍 Troubleshooting

### Common Issues

#### Model Loading Fails
```bash
# Check internet connection
curl -I https://huggingface.co

# Check disk space
df -h

# Clear model cache
docker volume rm dubsync_model_cache
```

#### GPU Not Detected
```bash
# Check NVIDIA drivers
nvidia-smi

# Check Docker GPU support
docker run --rm --gpus all nvidia/cuda:11.8-base-ubuntu20.04 nvidia-smi

# Use CPU fallback
docker-compose -f docker-compose.cpu.yml up
```

#### WebSocket Connection Issues
```bash
# Check Redis
docker-compose exec redis redis-cli ping

# Check ports
netstat -tlnp | grep :8000

# Check firewall
sudo ufw status
```

#### Audio Recording Issues
```bash
# Browser permissions
# Chrome: chrome://settings/content/microphone
# Firefox: about:preferences#privacy

# HTTPS requirement
# Use SSL certificate for production
# Use localhost for development
```

### Performance Optimization

#### GPU Memory
```bash
# Monitor GPU usage
nvidia-smi -l 1

# Adjust batch size in settings.py
# TRANSCRIPTION_BATCH_SIZE = 1  # Reduce for less memory
```

#### CPU Performance
```bash
# Increase worker processes
# In docker-compose.yml:
# command: daphne -b 0.0.0.0 -p 8000 --workers 4 dubsync_backend.asgi:application
```

## 📈 Scaling

### Horizontal Scaling
```bash
# Multiple backend instances
docker-compose up --scale backend=3

# Load balancer (nginx)
upstream backend {
    server backend:8000;
    server backend:8001;
    server backend:8002;
}
```

### Database Scaling
```bash
# PostgreSQL setup
# In docker-compose.yml:
services:
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: dubsync
      POSTGRES_USER: dubsync
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
```

## 🔒 Security

### Production Security
```bash
# Update secrets
SECRET_KEY=generate-new-secret-key
DATABASE_PASSWORD=strong-password

# Firewall rules
sudo ufw enable
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443

# Regular updates
sudo apt update && sudo apt upgrade
docker-compose pull && docker-compose up -d
```

### SSL/TLS
```bash
# Force HTTPS
# In settings.py:
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
```

---

For additional support, please refer to the [README.md](README.md) or open an issue on GitHub.