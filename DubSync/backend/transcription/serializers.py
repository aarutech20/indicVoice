from rest_framework import serializers
from .models import TranscriptionSession, TranscriptionResult

class TranscriptionSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TranscriptionSession
        fields = ['session_id', 'language_code', 'created_at', 'is_active']

class TranscriptionResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TranscriptionResult
        fields = ['chunk_number', 'transcription_text', 'confidence_score', 'timestamp']

class AudioChunkSerializer(serializers.Serializer):
    audio_data = serializers.CharField()  # Base64 encoded audio
    session_id = serializers.CharField(max_length=100)
    language_code = serializers.CharField(max_length=10)
    chunk_number = serializers.IntegerField()
    sample_rate = serializers.IntegerField(default=16000)

class LanguageSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=10)
    name = serializers.CharField(max_length=50)