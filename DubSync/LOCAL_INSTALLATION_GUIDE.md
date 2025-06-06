# 🎙️ IndicVoice - Local Installation Guide

## 📋 Complete Setup Instructions for Your Local System

This guide will help you set up and run the IndicVoice Real-Time Speech Transcription application on your local machine with full audio support.

## 🖥️ System Requirements

### Minimum Requirements:
- **OS**: Windows 10/11, macOS 10.15+, or Ubuntu 18.04+
- **RAM**: 4GB (8GB recommended)
- **Storage**: 5GB free space
- **Internet**: Required for initial model download
- **Microphone**: Any USB or built-in microphone

### Recommended Requirements:
- **RAM**: 8GB+ 
- **GPU**: NVIDIA GPU with 4GB+ VRAM (optional, for faster processing)
- **CPU**: Multi-core processor (Intel i5/AMD Ryzen 5 or better)

## 🛠️ Prerequisites Installation

### 1. Install Python 3.8+

#### Windows:
```bash
# Download from https://python.org/downloads/
# Or use chocolatey:
choco install python

# Verify installation
python --version
pip --version
```

#### macOS:
```bash
# Using Homebrew (recommended):
brew install python

# Or download from https://python.org/downloads/
# Verify installation
python3 --version
pip3 --version
```

#### Ubuntu/Linux:
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
sudo apt install python3-dev build-essential

# Verify installation
python3 --version
pip3 --version
```

### 2. Install Node.js 16+

#### Windows:
```bash
# Download from https://nodejs.org/
# Or use chocolatey:
choco install nodejs

# Verify installation
node --version
npm --version
```

#### macOS:
```bash
# Using Homebrew:
brew install node

# Verify installation
node --version
npm --version
```

#### Ubuntu/Linux:
```bash
# Using NodeSource repository:
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verify installation
node --version
npm --version
```

### 3. Install Git

#### Windows:
```bash
# Download from https://git-scm.com/
# Or use chocolatey:
choco install git
```

#### macOS:
```bash
# Usually pre-installed, or:
brew install git
```

#### Ubuntu/Linux:
```bash
sudo apt install git
```

### 4. Install Redis (Required for WebSocket support)

#### Windows:
```bash
# Download Redis for Windows from:
# https://github.com/microsoftarchive/redis/releases
# Or use chocolatey:
choco install redis-64
```

#### macOS:
```bash
brew install redis
```

#### Ubuntu/Linux:
```bash
sudo apt install redis-server
```

### 5. Install System Audio Dependencies

#### Windows:
```bash
# Usually included with Windows
# If issues, install Visual C++ Redistributable
```

#### macOS:
```bash
# Usually included with macOS
# If issues:
brew install portaudio
```

#### Ubuntu/Linux:
```bash
sudo apt install portaudio19-dev python3-pyaudio
sudo apt install alsa-utils pulseaudio
sudo apt install ffmpeg
```

## 📥 Project Installation

### Step 1: Clone the Repository
```bash
git clone https://github.com/aarutech20/indicVoice.git
cd indicVoice
```

### Step 2: Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install Python dependencies
pip install -r requirements.txt

# Set up database
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Test backend
python manage.py runserver 8000
```

### Step 3: Frontend Setup

Open a new terminal window:

```bash
# Navigate to frontend directory
cd indicVoice/frontend

# Install Node.js dependencies
npm install

# Start development server
npm run dev
```

### Step 4: Start Redis Server

Open another terminal window:

```bash
# Windows:
redis-server

# macOS:
brew services start redis

# Ubuntu/Linux:
sudo systemctl start redis-server
# Or:
redis-server
```

## 🚀 Running the Application

### Method 1: Development Mode (Recommended for testing)

1. **Start Redis** (in terminal 1):
```bash
redis-server
```

2. **Start Backend** (in terminal 2):
```bash
cd indicVoice/backend
source venv/bin/activate  # macOS/Linux
# or venv\Scripts\activate  # Windows
python manage.py runserver 8000
```

3. **Start Frontend** (in terminal 3):
```bash
cd indicVoice/frontend
npm run dev
```

4. **Open your browser** and go to: `http://localhost:3000`

### Method 2: Docker (Recommended for production)

#### Prerequisites:
- Install Docker Desktop from https://docker.com/products/docker-desktop

#### Run with Docker:
```bash
cd indicVoice

# Build and start all services
docker-compose up --build

# Access the application at http://localhost:3000
```

#### For GPU support:
```bash
# Install NVIDIA Docker runtime first
# Then use:
docker-compose -f docker-compose.gpu.yml up --build
```

## 🎤 Using the Application

### First Time Setup:

1. **Open the application** in your browser
2. **Allow microphone access** when prompted by your browser
3. **Select your preferred Indian language** from the dropdown
4. **Choose connection type**:
   - **HTTP API**: Standard mode
   - **WebSocket**: Real-time mode (recommended)

### Recording and Transcription:

1. **Click "Start Recording"**
2. **Speak clearly** into your microphone
3. **Watch real-time transcription** appear
4. **Use controls**:
   - **Clear**: Reset transcription
   - **Download**: Save as text file
   - **Stop**: End recording

## 🔧 Troubleshooting

### Common Issues:

#### 1. Microphone Not Working
```bash
# Check browser permissions
# Chrome: Settings > Privacy > Microphone
# Firefox: Preferences > Privacy > Permissions

# Test microphone in browser console:
navigator.mediaDevices.getUserMedia({audio: true})
```

#### 2. Backend Connection Error
```bash
# Check if backend is running:
curl http://localhost:8000/api/health/

# Check Django logs for errors
# Restart backend server
```

#### 3. Frontend Build Issues
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

#### 4. Redis Connection Error
```bash
# Check if Redis is running:
redis-cli ping

# Should return "PONG"
# If not, start Redis server
```

#### 5. Python Package Issues
```bash
# Update pip and reinstall
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

#### 6. Audio Processing Issues (Linux)
```bash
# Install additional audio libraries
sudo apt install libasound2-dev libportaudio2 libportaudiocpp0

# Check audio devices
arecord -l
```

### Performance Optimization:

#### For Better Performance:
1. **Use GPU**: Install CUDA and PyTorch with GPU support
2. **Increase RAM**: Close other applications
3. **Use SSD**: For faster model loading
4. **Stable Internet**: For initial model download

#### GPU Setup (Optional):
```bash
# Install CUDA (NVIDIA GPUs only)
# Download from: https://developer.nvidia.com/cuda-downloads

# Install PyTorch with CUDA
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

## 📊 Supported Languages

The application supports all 22 official Indian languages:

1. **Assamese** (as)
2. **Bengali** (bn)
3. **Bodo** (brx)
4. **Dogri** (doi)
5. **Gujarati** (gu)
6. **Hindi** (hi)
7. **Kannada** (kn)
8. **Konkani** (kok)
9. **Kashmiri** (ks)
10. **Maithili** (mai)
11. **Malayalam** (ml)
12. **Manipuri** (mni)
13. **Marathi** (mr)
14. **Nepali** (ne)
15. **Odia** (or)
16. **Punjabi** (pa)
17. **Sanskrit** (sa)
18. **Santali** (sat)
19. **Sindhi** (sd)
20. **Tamil** (ta)
21. **Telugu** (te)
22. **Urdu** (ur)

## 🔒 Security Notes

- The application runs locally on your machine
- Audio data is processed locally (not sent to external servers)
- Microphone access requires explicit browser permission
- All data stays on your local system

## 📱 Browser Compatibility

### Fully Supported:
- **Chrome** 60+ (Recommended)
- **Firefox** 55+
- **Edge** 79+
- **Safari** 11+ (limited WebRTC support)

### Features by Browser:
- **WebRTC Audio**: Chrome, Firefox, Edge
- **MediaRecorder API**: All modern browsers
- **WebSocket**: All modern browsers

## 🆘 Getting Help

### If you encounter issues:

1. **Check the logs**:
   - Backend: Terminal running Django server
   - Frontend: Browser Developer Console (F12)
   - Redis: Redis server terminal

2. **Common solutions**:
   - Restart all services
   - Clear browser cache
   - Check firewall settings
   - Verify microphone permissions

3. **Report issues**:
   - Create an issue on GitHub
   - Include error logs and system information

## 📈 Performance Expectations

### Typical Performance:
- **Latency**: 1-3 seconds
- **Accuracy**: 85-95% (depends on audio quality and language)
- **CPU Usage**: 20-50% during transcription
- **RAM Usage**: 2-4GB
- **GPU Usage**: 30-70% (if available)

### Tips for Better Accuracy:
- Speak clearly and at moderate pace
- Use a good quality microphone
- Minimize background noise
- Ensure stable internet for model download

---

## 🎉 You're Ready!

Once you've completed these steps, you'll have a fully functional real-time speech transcription system supporting 22 Indian languages running on your local machine!

**Happy Transcribing! 🎙️✨**