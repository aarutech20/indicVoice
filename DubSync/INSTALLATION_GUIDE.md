# 🚀 DubSync - Complete Installation & Setup Guide

## 📋 Table of Contents
1. [System Requirements](#system-requirements)
2. [Quick Start (Recommended)](#quick-start-recommended)
3. [Manual Installation](#manual-installation)
4. [Docker Installation](#docker-installation)
5. [Troubleshooting](#troubleshooting)
6. [Development Setup](#development-setup)

---

## 🖥️ System Requirements

### Minimum Requirements
- **OS**: Linux (Ubuntu 18.04+), macOS (10.15+), Windows 10/11
- **RAM**: 4GB (8GB recommended)
- **Storage**: 2GB free space
- **Internet**: Required for model download and dependencies

### Recommended Requirements
- **OS**: Ubuntu 20.04+ or macOS 12+
- **RAM**: 8GB+ (16GB for GPU usage)
- **GPU**: NVIDIA GPU with CUDA 11.8+ (optional but recommended)
- **Storage**: 5GB free space

---

## ⚡ Quick Start (Recommended)

### Option 1: Using Make Commands (Easiest)

```bash
# Clone the repository
git clone https://github.com/aarutech20/indicVoice.git
cd indicVoice

# Install everything and run (one command!)
make install-and-run

# Or step by step:
make install-system-deps    # Install system dependencies
make install-backend       # Install backend dependencies
make install-frontend      # Install frontend dependencies
make run-dev               # Run both backend and frontend
```

### Option 2: Quick Docker Setup

```bash
# Clone the repository
git clone https://github.com/aarutech20/indicVoice.git
cd indicVoice

# Run with Docker (CPU version)
docker-compose -f docker-compose.cpu.yml up --build

# Or GPU version (if you have NVIDIA GPU)
docker-compose up --build
```

**🎉 That's it! Open http://localhost:3000 in your browser**

---

## 🔧 Manual Installation

### Step 1: Install System Dependencies

#### Ubuntu/Debian:
```bash
# Update package list
sudo apt update

# Install required packages
sudo apt install -y \
    python3.10 \
    python3.10-venv \
    python3-pip \
    nodejs \
    npm \
    redis-server \
    ffmpeg \
    portaudio19-dev \
    git \
    curl \
    build-essential

# Start Redis
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

#### macOS:
```bash
# Install Homebrew if not installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install python@3.10 node npm redis ffmpeg portaudio git

# Start Redis
brew services start redis
```

#### Windows (WSL2 recommended):
```bash
# Install WSL2 and Ubuntu
wsl --install

# Then follow Ubuntu instructions above
```

### Step 2: Clone Repository
```bash
git clone https://github.com/aarutech20/indicVoice.git
cd indicVoice
```

### Step 3: Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python3.10 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env

# Run database migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Start backend server
python manage.py runserver 0.0.0.0:8000
```

### Step 4: Frontend Setup

```bash
# Open new terminal and navigate to frontend
cd frontend

# Install Node.js dependencies
npm install

# Set up environment variables
cp .env.example .env

# Start frontend development server
npm run dev
```

### Step 5: Access Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin

---

## 🐳 Docker Installation

### Prerequisites
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Add user to docker group (logout/login required)
sudo usermod -aG docker $USER
```

### CPU Version (Recommended for most users)
```bash
git clone https://github.com/aarutech20/indicVoice.git
cd indicVoice

# Build and run
docker-compose -f docker-compose.cpu.yml up --build

# Run in background
docker-compose -f docker-compose.cpu.yml up -d --build
```

### GPU Version (For NVIDIA GPU users)
```bash
# Install NVIDIA Docker support
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update && sudo apt-get install -y nvidia-docker2
sudo systemctl restart docker

# Run with GPU support
docker-compose up --build
```

---

## 🛠️ Troubleshooting

### Common Issues

#### 1. Port Already in Use
```bash
# Kill processes on ports 3000 and 8000
sudo lsof -ti:3000 | xargs kill -9
sudo lsof -ti:8000 | xargs kill -9

# Or use different ports
# Backend: python manage.py runserver 0.0.0.0:8001
# Frontend: npm run dev -- --port 3001
```

#### 2. Redis Connection Error
```bash
# Check Redis status
redis-cli ping

# Start Redis
sudo systemctl start redis-server  # Linux
brew services start redis          # macOS

# Or use Docker Redis
docker run -d -p 6379:6379 redis:alpine
```

#### 3. Python/Node Version Issues
```bash
# Check versions
python3 --version  # Should be 3.10+
node --version     # Should be 16+
npm --version      # Should be 8+

# Install correct versions using pyenv/nvm if needed
```

#### 4. Permission Errors
```bash
# Fix npm permissions
sudo chown -R $(whoami) ~/.npm
sudo chown -R $(whoami) /usr/local/lib/node_modules

# Fix Python permissions
sudo chown -R $(whoami) ~/.local
```

#### 5. Model Loading Issues
```bash
# Clear model cache
rm -rf ~/.cache/huggingface/
rm -rf ~/.cache/torch/

# Restart backend with verbose logging
DEBUG=True python manage.py runserver
```

### Performance Optimization

#### For Better Performance:
```bash
# Use GPU if available
export CUDA_VISIBLE_DEVICES=0

# Increase worker processes
export DJANGO_WORKERS=4

# Use production settings
export DJANGO_SETTINGS_MODULE=dubsync.settings.production
```

#### Memory Issues:
```bash
# Reduce model precision
export MODEL_PRECISION=float16

# Limit concurrent requests
export MAX_CONCURRENT_REQUESTS=2
```

---

## 👨‍💻 Development Setup

### Backend Development
```bash
cd backend

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python manage.py test

# Code formatting
black .
isort .

# Type checking
mypy .

# Run with auto-reload
python manage.py runserver --settings=dubsync.settings.development
```

### Frontend Development
```bash
cd frontend

# Install development dependencies
npm install --include=dev

# Run tests
npm test

# Code formatting
npm run format

# Type checking
npm run type-check

# Build for production
npm run build
```

### Environment Variables

#### Backend (.env):
```bash
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000
REDIS_URL=redis://localhost:6379/0
MODEL_CACHE_DIR=./models
CUDA_VISIBLE_DEVICES=0
```

#### Frontend (.env):
```bash
VITE_API_BASE_URL=http://localhost:8000/api
VITE_WS_BASE_URL=ws://localhost:8000/ws
VITE_APP_TITLE=DubSync
VITE_DEBUG=true
```

---

## 📱 Mobile/Tablet Support

The application works on mobile devices, but for best experience:

1. Use Chrome/Safari on mobile
2. Allow microphone permissions
3. Use headphones to prevent feedback
4. Ensure stable internet connection

---

## 🔒 Security Notes

1. **Never commit sensitive data** to version control
2. **Use HTTPS in production** environments
3. **Regularly update dependencies** for security patches
4. **Limit API access** in production
5. **Use environment variables** for all secrets

---

## 📞 Support

If you encounter issues:

1. Check this troubleshooting guide
2. Search existing GitHub issues
3. Create a new issue with:
   - Your OS and versions
   - Complete error messages
   - Steps to reproduce

---

## 🎯 Next Steps

After successful installation:

1. Test with different languages
2. Try both HTTP and WebSocket modes
3. Experiment with audio quality settings
4. Check the admin panel for monitoring
5. Read the API documentation

**Happy transcribing! 🎙️✨**