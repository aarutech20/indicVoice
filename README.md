# 🎙️ DubSync - Real-Time Speech Transcription

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A production-ready Streamlit application for **real-time speech transcription** supporting **22 Indian languages** using the IndicConformer model from AI4Bharat.

**🌟 GitHub Repository**: https://github.com/ARAVINDAN20/DubSync---Real-Time-Speech-Transcription

## 🌟 Features

- **Real-time transcription** with low latency (1-2 second chunks)
- **22 Indian languages** support via IndicConformer model
- **Live microphone input** with automatic speech detection
- **Modern Streamlit UI** with intuitive controls
- **GPU/CPU auto-detection** with fallback support
- **Docker containerization** for easy deployment
- **Production-ready** with proper error handling and logging
- **Download transcriptions** as text files
- **Voice Activity Detection (VAD)** for better accuracy

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit UI  │    │ Audio Processor │    │ IndicConformer  │
│                 │    │                 │    │     Model       │
│ • Language UI   │◄──►│ • Live Capture  │◄──►│ • CTC Decoder   │
│ • Controls      │    │ • VAD Detection │    │ • 22 Languages  │
│ • Live Display  │    │ • Preprocessing │    │ • GPU/CPU       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.9+**
- **Microphone** (built-in or external)
- **Internet connection** (for model download)
- **Optional**: NVIDIA GPU with CUDA for faster processing

### Option 1: Local Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ARAVINDAN20/DubSync---Real-Time-Speech-Transcription.git
   cd DubSync---Real-Time-Speech-Transcription
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser:**
   - Navigate to: http://localhost:8501
   - Allow microphone permissions when prompted

### Option 2: Docker Deployment

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ARAVINDAN20/DubSync---Real-Time-Speech-Transcription.git
   cd DubSync---Real-Time-Speech-Transcription
   ```

2. **Build and run with Docker:**
   ```bash
   # CPU version
   docker build -t dubsync .
   docker run -p 8501:8501 --device /dev/snd dubsync
   
   # Or use Docker Compose
   docker-compose up --build
   ```

3. **For GPU support:**
   ```bash
   # Requires NVIDIA Docker runtime
   docker-compose --profile gpu up --build
   ```

4. **Access the application:**
   - Navigate to: http://localhost:8501

## 🎯 Usage

### Basic Transcription

1. **Select Language**: Choose from 22 supported Indian languages in the sidebar
2. **Start Recording**: Click the "🎙️ Start Recording" button
3. **Speak**: Talk clearly into your microphone
4. **View Results**: Watch real-time transcriptions appear in the main area
5. **Stop Recording**: Click "⏹️ Stop Recording" when finished
6. **Download**: Export your transcriptions as a text file

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

## 🛠️ Development

### Project Structure

```
DubSync/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Container configuration
├── docker-compose.yml    # Multi-container setup
├── README.md            # This file
└── .gitignore           # Git ignore rules
```

### Key Components

1. **AudioProcessor Class**: Handles audio capture, preprocessing, and transcription
2. **Voice Activity Detection**: Uses WebRTC VAD for speech detection
3. **Model Integration**: Loads and manages the IndicConformer model
4. **Threading**: Non-blocking audio processing to keep UI responsive
5. **Streamlit UI**: Modern interface with real-time updates

### Environment Variables

```bash
# Optional environment variables
CUDA_VISIBLE_DEVICES=0          # GPU device selection
STREAMLIT_SERVER_PORT=8501      # Server port
STREAMLIT_SERVER_ADDRESS=0.0.0.0 # Server address
```

## 🔧 Configuration

### Audio Settings

- **Sample Rate**: 16 kHz (optimized for IndicConformer)
- **Channels**: Mono (single channel)
- **Chunk Duration**: 2 seconds for low latency
- **Buffer Size**: 10 seconds for continuous processing

### Model Settings

- **Model**: IndicConformer (AI4Bharat)
- **Decoder**: CTC (Connectionist Temporal Classification)
- **Device**: Auto-detection (CUDA → CPU fallback)
- **Precision**: Float32 for compatibility

## 🐳 Docker Commands

```bash
# Build the image
docker build -t dubsync .

# Run CPU version
docker run -p 8501:8501 --device /dev/snd dubsync

# Run with Docker Compose
docker-compose up --build

# Run GPU version (requires NVIDIA Docker)
docker-compose --profile gpu up --build

# View logs
docker-compose logs -f dubsync

# Stop services
docker-compose down
```

## 🔍 Troubleshooting

### Common Issues

1. **Microphone Not Working**
   - Grant microphone permissions in your browser
   - Check system audio settings
   - Ensure microphone is not used by other applications

2. **Model Loading Fails**
   - Check internet connection for model download
   - Verify available disk space (models can be large)
   - Try restarting the application

3. **Audio Quality Issues**
   - Use a good quality microphone
   - Minimize background noise
   - Speak clearly and at moderate pace
   - Ensure stable internet connection

4. **GPU Not Detected**
   - Install NVIDIA drivers and CUDA toolkit
   - Verify with `nvidia-smi` command
   - Application will automatically fallback to CPU

5. **Docker Audio Issues**
   - Ensure audio devices are properly mounted
   - Check Docker audio device permissions
   - Try running with `--privileged` flag if needed

### Performance Optimization

- **GPU Usage**: Significantly faster transcription with CUDA
- **Audio Quality**: 16kHz mono audio provides best results
- **Chunk Size**: 2-second chunks balance latency and accuracy
- **Memory**: Model caching reduces startup time

## 📊 Performance

- **Latency**: 200-500ms per chunk (GPU), 1-2s (CPU)
- **Accuracy**: Varies by language and audio quality
- **Memory Usage**: ~2-4GB RAM, ~2GB GPU VRAM
- **Supported Concurrent Users**: 1 (single-user application)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **AI4Bharat** for the IndicConformer model
- **Streamlit** for the amazing web framework
- **PyTorch** and **Transformers** for ML infrastructure
- **WebRTC** for voice activity detection
- **SoundDevice** for audio capture

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/ARAVINDAN20/DubSync---Real-Time-Speech-Transcription/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ARAVINDAN20/DubSync---Real-Time-Speech-Transcription/discussions)
- **Documentation**: This README and inline code comments

## 🔮 Future Enhancements

- [ ] Real-time translation between Indian languages
- [ ] Speaker identification and diarization
- [ ] Batch file processing
- [ ] Custom vocabulary support
- [ ] Mobile app development
- [ ] Cloud deployment options
- [ ] Multi-user support
- [ ] Audio quality enhancement

---

**Made with ❤️ for the Indian language community**

**🌟 Star this repository if you find it useful!**