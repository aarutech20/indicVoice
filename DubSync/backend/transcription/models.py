import numpy as np
import logging
import threading
import random
import time
from typing import Optional, Dict, Any
from django.db import models

logger = logging.getLogger(__name__)

class IndicConformerModel:
    """Singleton class to manage the IndicConformer model"""
    _instance = None
    _lock = threading.Lock()
    
    def __init__(self):
        self.model = None
        self.device = None
        self.is_loaded = False
        self._initialize_model()
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance
    
    def _initialize_model(self):
        """Initialize the demo IndicConformer model"""
        try:
            # Demo mode - always use CPU
            self.device = "cpu"
            logger.info("Demo mode: Using CPU device")
            
            # Demo model is always "loaded"
            self.model = "demo_model"
            self.is_loaded = True
            logger.info("Demo IndicConformer model initialized successfully")
                
        except Exception as e:
            logger.error(f"Failed to initialize demo model: {e}")
            self.is_loaded = False
    
    def _create_dummy_model(self):
        """Create a dummy model for development/testing"""
        logger.warning("Creating dummy model for development")
        self.model = None
        self.is_loaded = False
    
    def preprocess_audio(self, audio_data: np.ndarray, sample_rate: int) -> np.ndarray:
        """Demo audio preprocessing"""
        try:
            # Simple demo preprocessing - just return the input
            return audio_data
            
        except Exception as e:
            logger.error(f"Error preprocessing audio: {e}")
            raise
    
    def transcribe(self, audio_data: np.ndarray, sample_rate: int, language_code: str) -> str:
        """Transcribe audio data"""
        try:
            # Demo mode - simulate transcription
            import random
            import time
            
            # Demo language samples
            demo_samples = {
                'hi': ['नमस्ते, मैं हिंदी में बोल रहा हूं', 'यह एक परीक्षण है', 'आपका स्वागत है'],
                'bn': ['নমস্কার, আমি বাংলায় কথা বলছি', 'এটি একটি পরীক্ষা', 'আপনাকে স্বাগতম'],
                'ta': ['வணக்கம், நான் தமிழில் பேசுகிறேன்', 'இது ஒரு சோதனை', 'உங்களை வரவேற்கிறோம்'],
                'te': ['నమస్కారం, నేను తెలుగులో మాట్లాడుతున్నాను', 'ఇది ఒక పరీక్ష', 'మీకు స్వాగతం'],
                'gu': ['નમસ્તે, હું ગુજરાતીમાં બોલી રહ્યો છું', 'આ એક પરીક્ષણ છે', 'તમારું સ્વાગત છે'],
                'mr': ['नमस्कार, मी मराठीत बोलत आहे', 'ही एक चाचणी आहे', 'तुमचे स्वागत आहे'],
                'pa': ['ਸਤ ਸ੍ਰੀ ਅਕਾਲ, ਮੈਂ ਪੰਜਾਬੀ ਵਿੱਚ ਬੋਲ ਰਿਹਾ ਹਾਂ', 'ਇਹ ਇੱਕ ਟੈਸਟ ਹੈ', 'ਤੁਹਾਡਾ ਸੁਆਗਤ ਹੈ'],
                'kn': ['ನಮಸ್ಕಾರ, ನಾನು ಕನ್ನಡದಲ್ಲಿ ಮಾತನಾಡುತ್ತಿದ್ದೇನೆ', 'ಇದು ಒಂದು ಪರೀಕ್ಷೆ', 'ನಿಮಗೆ ಸ್ವಾಗತ'],
                'ml': ['നമസ്കാരം, ഞാൻ മലയാളത്തിൽ സംസാരിക്കുന്നു', 'ഇത് ഒരു പരീക്ഷണമാണ്', 'നിങ്ങളെ സ്വാഗതം ചെയ്യുന്നു'],
                'or': ['ନମସ୍କାର, ମୁଁ ଓଡ଼ିଆରେ କହୁଛି', 'ଏହା ଏକ ପରୀକ୍ଷା', 'ଆପଣଙ୍କୁ ସ୍ୱାଗତ'],
                'as': ['নমস্কাৰ, মই অসমীয়াত কৈছো', 'এইটো এটা পৰীক্ষা', 'আপোনাক স্বাগতম'],
                'ur': ['السلام علیکم، میں اردو میں بول رہا ہوں', 'یہ ایک ٹیسٹ ہے', 'آپ کا خیر مقدم']
            }
            
            # Simulate processing time
            time.sleep(random.uniform(0.5, 1.2))
            
            # Check if audio has content
            if len(audio_data) == 0 or np.max(np.abs(audio_data)) < 0.01:
                return ""
            
            # Get samples for the language
            samples = demo_samples.get(language_code, demo_samples['hi'])
            
            # Return a random sample
            return random.choice(samples)
                    
        except Exception as e:
            logger.error(f"Error during transcription: {e}")
            return f"Demo transcription for {language_code}"


class TranscriptionSession(models.Model):
    """Model to track transcription sessions"""
    session_id = models.CharField(max_length=100, unique=True)
    language_code = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Session {self.session_id} - {self.language_code}"


class TranscriptionResult(models.Model):
    """Model to store transcription results"""
    session = models.ForeignKey(TranscriptionSession, on_delete=models.CASCADE)
    chunk_number = models.IntegerField()
    transcription_text = models.TextField()
    confidence_score = models.FloatField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['chunk_number']
    
    def __str__(self):
        return f"Chunk {self.chunk_number}: {self.transcription_text[:50]}..."