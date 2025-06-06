import base64
import numpy as np
import logging
import uuid
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import IndicConformerModel, TranscriptionSession, TranscriptionResult
from .serializers import (
    AudioChunkSerializer, 
    TranscriptionSessionSerializer, 
    TranscriptionResultSerializer,
    LanguageSerializer
)

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

@api_view(['GET'])
def get_supported_languages(request):
    """Get list of supported languages"""
    languages = [
        {'code': code, 'name': name} 
        for code, name in LANGUAGE_MAPPING.items()
    ]
    return Response({'languages': languages})

@api_view(['GET'])
def health_check(request):
    """Health check endpoint"""
    model_instance = IndicConformerModel.get_instance()
    return Response({
        'status': 'healthy',
        'model_loaded': model_instance.is_loaded,
        'device': str(model_instance.device) if model_instance.device else 'unknown'
    })

@method_decorator(csrf_exempt, name='dispatch')
class TranscriptionView(APIView):
    """Main transcription endpoint"""
    
    def post(self, request):
        try:
            # Validate input data
            serializer = AudioChunkSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    {'error': 'Invalid input data', 'details': serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            data = serializer.validated_data
            
            # Decode base64 audio data
            try:
                audio_bytes = base64.b64decode(data['audio_data'])
                audio_array = np.frombuffer(audio_bytes, dtype=np.float32)
            except Exception as e:
                logger.error(f"Error decoding audio data: {e}")
                return Response(
                    {'error': 'Invalid audio data format'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Validate language code
            language_code = data['language_code']
            if language_code not in LANGUAGE_MAPPING:
                return Response(
                    {'error': f'Unsupported language code: {language_code}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Get or create transcription session
            session_id = data['session_id']
            session, created = TranscriptionSession.objects.get_or_create(
                session_id=session_id,
                defaults={
                    'language_code': language_code,
                    'is_active': True
                }
            )
            
            # Get model instance and transcribe
            model_instance = IndicConformerModel.get_instance()
            
            if len(audio_array) == 0:
                transcription_text = ""
            else:
                transcription_text = model_instance.transcribe(
                    audio_array, 
                    data['sample_rate'], 
                    language_code
                )
            
            # Save transcription result
            result = TranscriptionResult.objects.create(
                session=session,
                chunk_number=data['chunk_number'],
                transcription_text=transcription_text,
                confidence_score=None  # Could be added later
            )
            
            return Response({
                'session_id': session_id,
                'chunk_number': data['chunk_number'],
                'transcription': transcription_text,
                'language': LANGUAGE_MAPPING[language_code],
                'timestamp': result.timestamp.isoformat()
            })
            
        except Exception as e:
            logger.error(f"Error in transcription: {e}")
            return Response(
                {'error': 'Internal server error', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@api_view(['POST'])
def create_session(request):
    """Create a new transcription session"""
    try:
        language_code = request.data.get('language_code', 'hi')
        
        if language_code not in LANGUAGE_MAPPING:
            return Response(
                {'error': f'Unsupported language code: {language_code}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        session_id = str(uuid.uuid4())
        session = TranscriptionSession.objects.create(
            session_id=session_id,
            language_code=language_code,
            is_active=True
        )
        
        serializer = TranscriptionSessionSerializer(session)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        logger.error(f"Error creating session: {e}")
        return Response(
            {'error': 'Failed to create session'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
def end_session(request, session_id):
    """End a transcription session"""
    try:
        session = TranscriptionSession.objects.get(session_id=session_id)
        session.is_active = False
        session.save()
        
        return Response({'message': 'Session ended successfully'})
        
    except TranscriptionSession.DoesNotExist:
        return Response(
            {'error': 'Session not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        logger.error(f"Error ending session: {e}")
        return Response(
            {'error': 'Failed to end session'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def get_session_results(request, session_id):
    """Get all transcription results for a session"""
    try:
        session = TranscriptionSession.objects.get(session_id=session_id)
        results = TranscriptionResult.objects.filter(session=session).order_by('chunk_number')
        
        serializer = TranscriptionResultSerializer(results, many=True)
        return Response({
            'session_id': session_id,
            'language': LANGUAGE_MAPPING.get(session.language_code, 'Unknown'),
            'results': serializer.data
        })
        
    except TranscriptionSession.DoesNotExist:
        return Response(
            {'error': 'Session not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        logger.error(f"Error getting session results: {e}")
        return Response(
            {'error': 'Failed to get session results'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )