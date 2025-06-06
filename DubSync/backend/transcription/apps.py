from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)

class TranscriptionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'transcription'

    def ready(self):
        """Initialize the IndicConformer model when Django starts"""
        try:
            from .models import IndicConformerModel
            # Initialize the model singleton
            IndicConformerModel.get_instance()
            logger.info("IndicConformer model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load IndicConformer model: {e}")
            # Don't raise exception to allow Django to start even if model fails to load