# 🎙️ IndicVoice - Real-Time Speech Transcription

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![React 18](https://img.shields.io/badge/react-18+-blue.svg)](https://reactjs.org/)
[![Django 4.2](https://img.shields.io/badge/django-4.2+-green.svg)](https://www.djangoproject.com/)

A production-ready full-stack application for real-time speech transcription supporting **22 Indian languages** using AI4Bharat's IndicConformer model.

**🌟 Repository**: https://github.com/aarutech20/indicVoice

## 🌟 Features

- **Real-time transcription** with low latency (1-2 second chunks)
- **22 Indian languages** support via IndicConformer
- **Dual connectivity**: HTTP API and WebSocket for real-time streaming
- **Modern UI** with React and Bootstrap
- **GPU/CPU support** with automatic fallback
- **Docker containerization** for easy deployment
- **Production-ready** with proper error handling and logging

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend│    │  Django Backend │    │ IndicConformer  │
│                 │    │                 │    │     Model       │
│ • Audio Capture │◄──►│ • REST API      │◄──►│                 │
│ • WebSocket     │    │ • WebSocket     │    │ • CTC Decoder   │
│ • Live UI       │    │ • Audio Process │    │ • 22 Languages  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- **Docker & Docker Compose** (recommended)
- **Python 3.9+** (for local development)
- **Node.js 18+** (for frontend development)
- **NVIDIA GPU** (optional, CPU fallback available)

### Option 1: Docker Deployment (Recommended)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ARAVINDAN20/DubSync---Real-Time-Speech-Transcription.git
   cd DubSync---Real-Time-Speech-Transcription
   ```

2. **For GPU systems:**
   ```bash
   docker-compose up --build
   ```

3. **For CPU-only systems:**
   ```bash
   docker-compose -f docker-compose.cpu.yml up --build
   ```

4. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000/api
   - Admin Panel: http://localhost:8000/admin (admin/admin123)

### Option 2: Local Development

#### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Run migrations:**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Start Redis (required for WebSocket):**
   ```bash
   redis-server
   ```

7. **Start Django server:**
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

#### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start development server:**
   ```bash
   npm run dev
   ```

4. **Access application:**
   - Frontend: http://localhost:3000
   - Backend: http://localhost:8000

## 🎯 Usage

### Basic Transcription

1. **Select Language**: Choose from 22 supported Indian languages
2. **Choose Mode**: HTTP API (reliable) or WebSocket (real-time)
3. **Start Recording**: Click "Start Recording" and speak
4. **View Results**: See live transcriptions appear in real-time
5. **Download**: Export transcriptions as text file

### Supported Languages

| Language | Code | Language | Code | Language | Code |
|----------|------|----------|------|----------|------|
| Assamese | `as` | Bengali | `bn` | Bodo | `brx` |
| Dogri | `doi` | Gujarati | `gu` | Hindi | `hi` |
| Kannada | `kn` | Konkani | `kok` | Kashmiri | `ks` |
| Maithili | `mai` | Malayalam | `ml` | Manipuri | `mni` |
| Marathi | `mr` | Nepali | `ne` | Odia | `or` |
| Punjabi | `pa` | Sanskrit | `sa` | Santali | `sat` |
| Sindhi | `sd` | Tamil | `ta` | Telugu | `te` |
| Urdu | `ur` | | | | |

## 🔧 API Reference

### REST Endpoints

- `GET /api/health/` - Health check
- `GET /api/languages/` - Get supported languages
- `POST /api/session/create/` - Create transcription session
- `POST /api/transcribe/` - Transcribe audio chunk
- `POST /api/session/{id}/end/` - End session

### WebSocket

- `ws://localhost:8000/ws/transcription/{session_id}/`

**Message Types:**
```javascript
// Send audio chunk
{
  "type": "audio_chunk",
  "audio_data": "base64_encoded_audio",
  "language_code": "hi",
  "chunk_number": 1
}

// Receive transcription
{
  "type": "transcription_result",
  "transcription": "transcribed text",
  "chunk_number": 1
}
```

## 🛠️ Development

### Project Structure

```
DubSync/
├── backend/                 # Django backend
│   ├── dubsync_backend/    # Django project
│   ├── transcription/      # Main app
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile         # Backend container
├── frontend/               # React frontend
│   ├── src/               # Source code
│   ├── public/            # Static assets
│   ├── package.json       # Node dependencies
│   └── Dockerfile         # Frontend container
├── docker-compose.yml     # GPU deployment
├── docker-compose.cpu.yml # CPU deployment
└── README.md             # This file
```

### Environment Variables

**Backend (.env):**
```env
SECRET_KEY=your-secret-key
DEBUG=True
REDIS_URL=redis://localhost:6379/0
CUDA_VISIBLE_DEVICES=0
```

**Frontend:**
```env
VITE_API_BASE_URL=http://localhost:8000/api
```

### Adding New Languages

1. Update `LANGUAGE_MAPPING` in `transcription/views.py`
2. Ensure IndicConformer model supports the language
3. Test transcription accuracy

## 🐳 Docker Commands

```bash
# Build and start all services
docker-compose up --build

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Stop services
docker-compose down

# Remove volumes (reset data)
docker-compose down -v
```

## 🔍 Troubleshooting

### Common Issues

1. **Model Loading Fails**
   - Check internet connection for model download
   - Verify CUDA/PyTorch installation
   - Check available disk space

2. **Audio Not Recording**
   - Grant microphone permissions in browser
   - Check browser compatibility (Chrome/Firefox recommended)
   - Verify HTTPS for production deployment

3. **WebSocket Connection Fails**
   - Ensure Redis is running
   - Check firewall settings
   - Verify WebSocket URL configuration

4. **GPU Not Detected**
   - Install NVIDIA Docker runtime
   - Check `nvidia-smi` output
   - Use CPU version if GPU unavailable

### Performance Optimization

- **GPU Memory**: Adjust batch size for available VRAM
- **Audio Quality**: Use 16kHz mono audio for best results
- **Network**: Use WebSocket for lowest latency
- **Caching**: Model loads once and stays in memory

## 📊 Performance

- **Latency**: 200-500ms per chunk (GPU), 1-2s (CPU)
- **Accuracy**: Varies by language and audio quality
- **Throughput**: ~10 concurrent sessions (GPU), ~3 (CPU)
- **Memory**: ~4GB GPU VRAM, ~8GB RAM

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **AI4Bharat** for the IndicConformer model
- **NVIDIA NeMo** for the ASR framework
- **Django** and **React** communities
- **Contributors** and **testers**

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/ARAVINDAN20/DubSync---Real-Time-Speech-Transcription/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ARAVINDAN20/DubSync---Real-Time-Speech-Transcription/discussions)
- **Email**: support@dubsync.com

---

**Made with ❤️ for the Indian language community**