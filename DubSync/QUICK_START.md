# 🚀 IndicVoice - Quick Start Guide

Get IndicVoice running on your local machine in under 10 minutes!

## ⚡ Super Quick Setup (3 Commands)

```bash
# 1. Clone the repository
git clone https://github.com/aarutech20/indicVoice.git
cd indicVoice

# 2. Run with Docker (Recommended)
docker-compose up --build

# 3. Open your browser
# Go to: http://localhost:3000
```

**That's it! 🎉** Your IndicVoice application is now running!

---

## 🛠️ Manual Setup (If you prefer not to use Docker)

### Prerequisites:
- Python 3.8+
- Node.js 16+
- Redis server

### Setup Steps:

#### 1. Backend Setup
```bash
cd backend
python -m venv venv

# Activate virtual environment:
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 8000
```

#### 2. Frontend Setup (New Terminal)
```bash
cd frontend
npm install
npm run dev
```

#### 3. Start Redis (New Terminal)
```bash
# Windows: redis-server
# macOS: brew services start redis
# Linux: sudo systemctl start redis-server
redis-server
```

#### 4. Open Browser
Go to: `http://localhost:3000`

---

## 🎤 How to Use

1. **Allow microphone access** when prompted
2. **Select your language** from the dropdown (22 Indian languages)
3. **Click "Start Recording"**
4. **Speak into your microphone**
5. **Watch real-time transcription** appear!

---

## 🔧 Troubleshooting

### Issue: Microphone not working
**Solution**: Check browser permissions for microphone access

### Issue: Backend connection error
**Solution**: Ensure backend is running on port 8000

### Issue: Redis connection error
**Solution**: Start Redis server

---

## 📚 Need More Help?

- **Detailed Setup**: See [LOCAL_INSTALLATION_GUIDE.md](LOCAL_INSTALLATION_GUIDE.md)
- **Full Documentation**: See [README.md](README.md)
- **Deployment Guide**: See [DEPLOYMENT.md](docs/DEPLOYMENT.md)

---

**Happy Transcribing! 🎙️✨**