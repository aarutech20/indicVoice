# 🚀 DubSync - Local Running Instructions

## 🎯 Quick Start (5 Minutes Setup)

### Step 1: Clone Repository
```bash
git clone https://github.com/aarutech20/indicVoice.git
cd indicVoice
```

### Step 2: One-Command Setup (Recommended)
```bash
# Install everything and run (works on Ubuntu/macOS)
make install-and-run
```

**OR follow manual steps below:**

---

## 🔧 Manual Setup

### Prerequisites Check
```bash
# Verify you have required tools
python3 --version  # Should be 3.10+
node --version     # Should be 16+
npm --version      # Should be 8+
redis-cli ping     # Should return PONG
```

### Install Missing Prerequisites

#### Ubuntu/Debian:
```bash
sudo apt update
sudo apt install -y python3.10 python3.10-venv python3-pip nodejs npm redis-server ffmpeg portaudio19-dev
sudo systemctl start redis-server
```

#### macOS:
```bash
brew install python@3.10 node npm redis ffmpeg portaudio
brew services start redis
```

#### Windows (Use WSL2):
```bash
wsl --install
# Then follow Ubuntu instructions
```

---

## 🖥️ Running the Application

### Method 1: Using Make Commands (Easiest)
```bash
# Install all dependencies
make install-all

# Run both backend and frontend
make run-dev

# Or run separately:
make run-backend    # Terminal 1
make run-frontend   # Terminal 2
```

### Method 2: Manual Commands

#### Terminal 1 - Backend Setup:
```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Setup environment
cp .env.example .env

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver 0.0.0.0:8000
```

#### Terminal 2 - Frontend Setup:
```bash
cd frontend

# Install dependencies
npm install

# Setup environment
cp .env.example .env

# Start development server
npm run dev
```

---

## 🌐 Access Your Application

Once both servers are running:

- **🎙️ Main App**: http://localhost:3000
- **🔧 Backend API**: http://localhost:8000
- **👨‍💼 Admin Panel**: http://localhost:8000/admin
- **📊 API Docs**: http://localhost:8000/api/docs

---

## 🎮 How to Use DubSync

### 1. Select Language
- Open http://localhost:3000
- Choose from 22 Indian languages in dropdown
- Languages include: Hindi, Tamil, Telugu, Bengali, etc.

### 2. Choose Connection Mode
- **WebSocket (Real-time)**: For instant transcription
- **HTTP API**: For stable connection (default)

### 3. Start Recording
- Click "Start Recording" button
- Allow microphone permissions when prompted
- Speak in your selected language

### 4. View Transcriptions
- See live transcriptions appear in real-time
- Each line shows timestamp and text
- Use "Clear" to reset or "Download" to save

---

## 🐳 Docker Alternative

If you prefer Docker:

```bash
# CPU version (recommended)
docker-compose -f docker-compose.cpu.yml up --build

# GPU version (if you have NVIDIA GPU)
docker-compose up --build

# Access at http://localhost:3000
```

---

## ✅ Current Status & Features

### ✅ Working Features:
- ✅ Real-time audio recording from microphone
- ✅ 22 Indian language support
- ✅ Live transcription display
- ✅ WebSocket real-time mode
- ✅ HTTP API fallback mode
- ✅ Session management
- ✅ Download transcriptions as text
- ✅ Responsive web interface
- ✅ Auto device detection (CPU/GPU)

### 🔄 Current Mode:
**Demo Mode**: Running with sample transcriptions for immediate testing
- Pre-built responses for 12+ Indian languages
- Simulates real transcription for development/testing
- Perfect for UI/UX testing and demonstrations

### 🚀 Production Mode:
To enable full IndicConformer model:
```bash
# Install additional ML dependencies
cd backend
pip install torch torchaudio transformers nemo-toolkit

# Update settings to use real model
export USE_REAL_MODEL=true

# Restart backend
python manage.py runserver 0.0.0.0:8000
```

---

## 🛠️ Troubleshooting

### Common Issues & Solutions:

#### 1. **Port Already in Use**
```bash
# Kill processes on busy ports
sudo lsof -ti:3000,8000 | xargs kill -9

# Or use different ports
python manage.py runserver 0.0.0.0:8001  # Backend
npm run dev -- --port 3001               # Frontend
```

#### 2. **Redis Connection Error**
```bash
# Check Redis status
redis-cli ping

# Start Redis
sudo systemctl start redis-server  # Linux
brew services start redis          # macOS

# Or use Docker Redis
docker run -d -p 6379:6379 redis:alpine
```

#### 3. **Microphone Not Working**
- Check browser permissions (click lock icon in address bar)
- Use HTTPS in production (required for microphone access)
- Try different browsers (Chrome/Firefox recommended)
- Check system microphone settings

#### 4. **Dependencies Issues**
```bash
# Clear npm cache
npm cache clean --force

# Clear pip cache
pip cache purge

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install

rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 5. **Permission Errors**
```bash
# Fix npm permissions
sudo chown -R $(whoami) ~/.npm

# Fix Python permissions
sudo chown -R $(whoami) ~/.local
```

---

## 📊 Performance Tips

### For Better Performance:
```bash
# Use GPU if available
export CUDA_VISIBLE_DEVICES=0

# Increase workers
export DJANGO_WORKERS=4

# Enable production optimizations
export DJANGO_SETTINGS_MODULE=dubsync.settings.production
```

### Memory Optimization:
```bash
# Reduce model precision
export MODEL_PRECISION=float16

# Limit concurrent requests
export MAX_CONCURRENT_REQUESTS=2
```

---

## 🔍 Development & Testing

### Backend Testing:
```bash
cd backend
python manage.py test
python manage.py check
```

### Frontend Testing:
```bash
cd frontend
npm test
npm run build  # Test production build
```

### API Testing:
```bash
# Test health endpoint
curl http://localhost:8000/api/health/

# Test transcription endpoint
curl -X POST http://localhost:8000/api/transcribe/ \
  -H "Content-Type: application/json" \
  -d '{"language": "hi", "text": "test"}'
```

---

## 📱 Mobile Support

The app works on mobile devices:
- Use Chrome/Safari on mobile
- Allow microphone permissions
- Use headphones to prevent feedback
- Ensure stable internet connection

---

## 🆘 Getting Help

If you encounter issues:

1. **Check logs**:
   ```bash
   # Backend logs
   tail -f backend/logs/django.log
   
   # Frontend logs
   # Check browser console (F12)
   ```

2. **Common solutions**:
   - Restart both servers
   - Clear browser cache
   - Check firewall settings
   - Verify all dependencies installed

3. **Create GitHub issue** with:
   - Your OS and versions
   - Complete error messages
   - Steps to reproduce

---

## 🎉 Success!

If everything is working, you should see:
- ✅ Backend server running on http://localhost:8000
- ✅ Frontend app running on http://localhost:3000
- ✅ Redis server connected
- ✅ Microphone access granted
- ✅ Language selection working
- ✅ Real-time transcription active

**Happy transcribing! 🎙️✨**

---

## 📚 Additional Resources

- [Complete Installation Guide](./INSTALLATION_GUIDE.md)
- [API Documentation](http://localhost:8000/api/docs)
- [Project Architecture](./PROJECT_SUMMARY.md)
- [Deployment Guide](./DEPLOYMENT.md)
- [Contributing Guidelines](./CONTRIBUTING.md)