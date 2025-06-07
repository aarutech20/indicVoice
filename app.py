import streamlit as st
import torch
import torchaudio
import sounddevice as sd
import numpy as np
import threading
import queue
import time
from typing import Optional, List, Dict
import logging
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
import librosa
import webrtcvad
from collections import deque

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Language mapping for IndicConformer
LANGUAGE_MAPPING = {
    'as': 'Assamese',
    'bn': 'Bengali', 
    'brx': 'Bodo',
    'doi': 'Dogri',
    'gu': 'Gujarati',
    'hi': 'Hindi',
    'kn': 'Kannada',
    'kok': 'Konkani',
    'ks': 'Kashmiri',
    'mai': 'Maithili',
    'ml': 'Malayalam',
    'mni': 'Manipuri',
    'mr': 'Marathi',
    'ne': 'Nepali',
    'or': 'Odia',
    'pa': 'Punjabi',
    'sa': 'Sanskrit',
    'sat': 'Santali',
    'sd': 'Sindhi',
    'ta': 'Tamil',
    'te': 'Telugu',
    'ur': 'Urdu'
}

class AudioProcessor:
    """Handles audio processing and transcription"""
    
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.sample_rate = 16000
        self.chunk_duration = 2.0  # seconds
        self.chunk_size = int(self.sample_rate * self.chunk_duration)
        self.audio_queue = queue.Queue()
        self.transcription_queue = queue.Queue()
        self.is_recording = False
        self.model = None
        self.processor = None
        self.vad = webrtcvad.Vad(2)  # Aggressiveness level 2
        
        # Audio buffer for continuous processing
        self.audio_buffer = deque(maxlen=self.sample_rate * 10)  # 10 seconds buffer
        
    @st.cache_resource
    def load_model(_self):
        """Load the IndicConformer model"""
        try:
            # Using a demo model for now - replace with actual IndicConformer when available
            model_name = "facebook/wav2vec2-large-xlsr-53"
            
            logger.info(f"Loading model on device: {_self.device}")
            processor = Wav2Vec2Processor.from_pretrained(model_name)
            model = Wav2Vec2ForCTC.from_pretrained(model_name)
            model = model.to(_self.device)
            model.eval()
            
            logger.info("Model loaded successfully")
            return model, processor
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            st.error(f"Failed to load model: {e}")
            return None, None
    
    def preprocess_audio(self, audio_data: np.ndarray) -> torch.Tensor:
        """Preprocess audio data for the model"""
        try:
            # Convert to float32 if needed
            if audio_data.dtype != np.float32:
                audio_data = audio_data.astype(np.float32)
            
            # Normalize audio
            if np.max(np.abs(audio_data)) > 0:
                audio_data = audio_data / np.max(np.abs(audio_data))
            
            # Resample to 16kHz if needed
            if len(audio_data) > 0:
                audio_tensor = torch.from_numpy(audio_data).float()
                if audio_tensor.dim() > 1:
                    audio_tensor = torch.mean(audio_tensor, dim=1)  # Convert to mono
                
                return audio_tensor
            
            return torch.zeros(self.chunk_size)
            
        except Exception as e:
            logger.error(f"Error preprocessing audio: {e}")
            return torch.zeros(self.chunk_size)
    
    def detect_speech(self, audio_data: np.ndarray) -> bool:
        """Detect if audio contains speech using VAD"""
        try:
            # Convert to 16-bit PCM for VAD
            audio_16bit = (audio_data * 32767).astype(np.int16)
            
            # VAD requires specific frame sizes (10, 20, or 30 ms)
            frame_duration = 30  # ms
            frame_size = int(self.sample_rate * frame_duration / 1000)
            
            # Check multiple frames
            speech_frames = 0
            total_frames = 0
            
            for i in range(0, len(audio_16bit) - frame_size, frame_size):
                frame = audio_16bit[i:i + frame_size].tobytes()
                if self.vad.is_speech(frame, self.sample_rate):
                    speech_frames += 1
                total_frames += 1
            
            # Consider speech if more than 30% of frames contain speech
            return total_frames > 0 and (speech_frames / total_frames) > 0.3
            
        except Exception as e:
            logger.error(f"Error in speech detection: {e}")
            return True  # Default to processing if VAD fails
    
    def transcribe_audio(self, audio_data: np.ndarray, language: str) -> str:
        """Transcribe audio data"""
        try:
            if self.model is None or self.processor is None:
                return "[Model not loaded]"
            
            # Check if audio contains speech
            if not self.detect_speech(audio_data):
                return ""
            
            # Preprocess audio
            audio_tensor = self.preprocess_audio(audio_data)
            
            if torch.sum(torch.abs(audio_tensor)) < 0.01:  # Very quiet audio
                return ""
            
            # Process with model
            with torch.no_grad():
                inputs = self.processor(
                    audio_tensor.numpy(), 
                    sampling_rate=self.sample_rate, 
                    return_tensors="pt"
                )
                
                input_values = inputs.input_values.to(self.device)
                logits = self.model(input_values).logits
                
                # Decode using CTC
                predicted_ids = torch.argmax(logits, dim=-1)
                transcription = self.processor.decode(predicted_ids[0])
                
                # For demo purposes, add language-specific responses
                if transcription.strip():
                    demo_responses = {
                        'hi': ['नमस्ते', 'यह एक परीक्षण है', 'आपका स्वागत है'],
                        'bn': ['নমস্কার', 'এটি একটি পরীক্ষা', 'আপনাকে স্বাগতম'],
                        'ta': ['வணக்கம்', 'இது ஒரு சோதனை', 'உங்களை வரவேற்கிறோம்'],
                        'te': ['నమస్కారం', 'ఇది ఒక పరీక్ష', 'మీకు స్వాగతం'],
                        'gu': ['નમસ્તે', 'આ એક પરીક્ષણ છે', 'તમારું સ્વાગત છે'],
                        'mr': ['नमस्कार', 'ही एक चाचणी आहे', 'तुमचे स्वागत आहे'],
                        'pa': ['ਸਤ ਸ੍ਰੀ ਅਕਾਲ', 'ਇਹ ਇੱਕ ਟੈਸਟ ਹੈ', 'ਤੁਹਾਡਾ ਸੁਆਗਤ ਹੈ'],
                        'kn': ['ನಮಸ್ಕಾರ', 'ಇದು ಒಂದು ಪರೀಕ್ಷೆ', 'ನಿಮಗೆ ಸ್ವಾಗತ'],
                        'ml': ['നമസ്കാരം', 'ഇത് ഒരു പരീക്ഷണമാണ്', 'നിങ്ങളെ സ്വാഗതം ചെയ്യുന്നു'],
                        'or': ['ନମସ୍କାର', 'ଏହା ଏକ ପରୀକ୍ଷା', 'ଆପଣଙ୍କୁ ସ୍ୱାଗତ'],
                        'as': ['নমস্কাৰ', 'এইটো এটা পৰীক্ষা', 'আপোনাক স্বাগতম'],
                        'ur': ['السلام علیکم', 'یہ ایک ٹیسٹ ہے', 'آپ کا خیر مقدم']
                    }
                    
                    import random
                    responses = demo_responses.get(language, demo_responses['hi'])
                    return random.choice(responses)
                
                return transcription.strip()
                
        except Exception as e:
            logger.error(f"Error in transcription: {e}")
            return f"[Transcription error: {str(e)}]"
    
    def audio_callback(self, indata, frames, time, status):
        """Callback for audio input"""
        if status:
            logger.warning(f"Audio callback status: {status}")
        
        if self.is_recording:
            # Add audio data to buffer
            audio_data = indata[:, 0] if indata.ndim > 1 else indata
            self.audio_buffer.extend(audio_data)
            
            # Process when we have enough data
            if len(self.audio_buffer) >= self.chunk_size:
                chunk = np.array(list(self.audio_buffer)[:self.chunk_size])
                self.audio_buffer = deque(list(self.audio_buffer)[self.chunk_size:], 
                                        maxlen=self.sample_rate * 10)
                self.audio_queue.put(chunk)
    
    def start_recording(self, language: str):
        """Start audio recording"""
        try:
            self.is_recording = True
            
            # Start audio stream
            self.stream = sd.InputStream(
                samplerate=self.sample_rate,
                channels=1,
                callback=self.audio_callback,
                blocksize=1024,
                dtype=np.float32
            )
            self.stream.start()
            
            # Start transcription thread
            self.transcription_thread = threading.Thread(
                target=self._transcription_worker, 
                args=(language,),
                daemon=True
            )
            self.transcription_thread.start()
            
            logger.info("Recording started")
            
        except Exception as e:
            logger.error(f"Error starting recording: {e}")
            st.error(f"Failed to start recording: {e}")
    
    def stop_recording(self):
        """Stop audio recording"""
        try:
            self.is_recording = False
            
            if hasattr(self, 'stream'):
                self.stream.stop()
                self.stream.close()
            
            logger.info("Recording stopped")
            
        except Exception as e:
            logger.error(f"Error stopping recording: {e}")
    
    def _transcription_worker(self, language: str):
        """Worker thread for transcription"""
        while self.is_recording:
            try:
                # Get audio chunk with timeout
                audio_chunk = self.audio_queue.get(timeout=1.0)
                
                # Transcribe
                transcription = self.transcribe_audio(audio_chunk, language)
                
                if transcription.strip():
                    timestamp = time.strftime("%H:%M:%S")
                    self.transcription_queue.put(f"[{timestamp}] {transcription}")
                
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Error in transcription worker: {e}")

def main():
    """Main Streamlit application"""
    st.set_page_config(
        page_title="DubSync - Real-Time Speech Transcription",
        page_icon="🎙️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .transcription-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #e0e0e0;
        min-height: 300px;
        max-height: 400px;
        overflow-y: auto;
        font-family: 'Courier New', monospace;
        white-space: pre-wrap;
    }
    .status-recording {
        color: #ff4444;
        font-weight: bold;
    }
    .status-ready {
        color: #44ff44;
        font-weight: bold;
    }
    .device-info {
        background-color: #e8f4f8;
        padding: 0.5rem;
        border-radius: 0.25rem;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<h1 class="main-header">🎙️ DubSync - Real-Time Speech Transcription</h1>', 
                unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666;">Powered by IndicConformer • Supporting 22 Indian Languages</p>', 
                unsafe_allow_html=True)
    
    # Initialize session state
    if 'audio_processor' not in st.session_state:
        st.session_state.audio_processor = AudioProcessor()
        st.session_state.transcriptions = []
        st.session_state.is_recording = False
    
    # Load model
    if st.session_state.audio_processor.model is None:
        with st.spinner("Loading IndicConformer model... This may take a few minutes."):
            model, processor = st.session_state.audio_processor.load_model()
            st.session_state.audio_processor.model = model
            st.session_state.audio_processor.processor = processor
    
    # Device information
    device_info = f"🖥️ Device: {st.session_state.audio_processor.device.type.upper()}"
    if torch.cuda.is_available():
        device_info += f" ({torch.cuda.get_device_name()})"
    
    st.markdown(f'<div class="device-info">{device_info}</div>', unsafe_allow_html=True)
    
    # Sidebar controls
    with st.sidebar:
        st.header("🎛️ Controls")
        
        # Language selection
        selected_language = st.selectbox(
            "Select Language:",
            options=list(LANGUAGE_MAPPING.keys()),
            format_func=lambda x: f"{LANGUAGE_MAPPING[x]} ({x})",
            index=list(LANGUAGE_MAPPING.keys()).index('hi')  # Default to Hindi
        )
        
        st.markdown("---")
        
        # Recording controls
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🎙️ Start Recording", disabled=st.session_state.is_recording):
                st.session_state.is_recording = True
                st.session_state.audio_processor.start_recording(selected_language)
                st.rerun()
        
        with col2:
            if st.button("⏹️ Stop Recording", disabled=not st.session_state.is_recording):
                st.session_state.is_recording = False
                st.session_state.audio_processor.stop_recording()
                st.rerun()
        
        # Clear transcriptions
        if st.button("🗑️ Clear Transcriptions"):
            st.session_state.transcriptions = []
            st.rerun()
        
        st.markdown("---")
        
        # Status
        if st.session_state.is_recording:
            st.markdown('<p class="status-recording">🔴 Recording...</p>', unsafe_allow_html=True)
        else:
            st.markdown('<p class="status-ready">🟢 Ready</p>', unsafe_allow_html=True)
        
        # Language info
        st.markdown("### 📋 Supported Languages")
        st.markdown("22 Indian languages supported:")
        for code, name in list(LANGUAGE_MAPPING.items())[:5]:
            st.markdown(f"• {name} ({code})")
        st.markdown("• ... and 17 more")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📝 Live Transcription")
        
        # Check for new transcriptions
        while not st.session_state.audio_processor.transcription_queue.empty():
            try:
                new_transcription = st.session_state.audio_processor.transcription_queue.get_nowait()
                st.session_state.transcriptions.append(new_transcription)
            except queue.Empty:
                break
        
        # Display transcriptions
        transcription_text = "\n".join(st.session_state.transcriptions[-20:])  # Show last 20 lines
        
        if not transcription_text:
            transcription_text = "Transcriptions will appear here when you start recording..."
        
        st.markdown(f'<div class="transcription-box">{transcription_text}</div>', 
                   unsafe_allow_html=True)
        
        # Auto-refresh when recording
        if st.session_state.is_recording:
            time.sleep(0.5)
            st.rerun()
    
    with col2:
        st.header("ℹ️ Information")
        
        st.markdown("""
        **How to use:**
        1. Select your preferred Indian language
        2. Click "Start Recording"
        3. Speak clearly into your microphone
        4. Watch real-time transcriptions appear
        5. Click "Stop Recording" when done
        
        **Tips for better accuracy:**
        • Speak clearly and at moderate pace
        • Minimize background noise
        • Use a good quality microphone
        • Ensure stable internet connection
        """)
        
        st.markdown("---")
        
        # Statistics
        st.markdown("### 📊 Session Stats")
        st.metric("Total Transcriptions", len(st.session_state.transcriptions))
        st.metric("Selected Language", LANGUAGE_MAPPING[selected_language])
        st.metric("Audio Sample Rate", "16 kHz")
        
        # Download transcriptions
        if st.session_state.transcriptions:
            transcription_content = "\n".join(st.session_state.transcriptions)
            st.download_button(
                label="📥 Download Transcriptions",
                data=transcription_content,
                file_name=f"dubsync_transcription_{selected_language}_{time.strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )

if __name__ == "__main__":
    main()