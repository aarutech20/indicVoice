import json
import base64
import numpy as np
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import IndicConformerModel, TranscriptionSession, TranscriptionResult

logger = logging.getLogger(__name__)

class TranscriptionConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for real-time transcription"""
    
    async def connect(self):
        self.session_id = self.scope['url_route']['kwargs']['session_id']
        self.room_group_name = f'transcription_{self.session_id}'
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Send connection confirmation
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'session_id': self.session_id
        }))
    
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message_type = data.get('type')
            
            if message_type == 'audio_chunk':
                await self.handle_audio_chunk(data)
            elif message_type == 'start_session':
                await self.handle_start_session(data)
            elif message_type == 'end_session':
                await self.handle_end_session(data)
            else:
                await self.send(text_data=json.dumps({
                    'type': 'error',
                    'message': f'Unknown message type: {message_type}'
                }))
                
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Invalid JSON format'
            }))
        except Exception as e:
            logger.error(f"Error in WebSocket receive: {e}")
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Internal server error'
            }))
    
    async def handle_audio_chunk(self, data):
        """Handle incoming audio chunk for transcription"""
        try:
            # Extract audio data
            audio_data = data.get('audio_data')
            language_code = data.get('language_code', 'hi')
            chunk_number = data.get('chunk_number', 0)
            sample_rate = data.get('sample_rate', 16000)
            
            if not audio_data:
                await self.send(text_data=json.dumps({
                    'type': 'error',
                    'message': 'No audio data provided'
                }))
                return
            
            # Decode audio data
            audio_bytes = base64.b64decode(audio_data)
            audio_array = np.frombuffer(audio_bytes, dtype=np.float32)
            
            # Get transcription
            transcription = await self.transcribe_audio(
                audio_array, sample_rate, language_code, chunk_number
            )
            
            # Send transcription result
            await self.send(text_data=json.dumps({
                'type': 'transcription_result',
                'session_id': self.session_id,
                'chunk_number': chunk_number,
                'transcription': transcription,
                'language_code': language_code
            }))
            
        except Exception as e:
            logger.error(f"Error handling audio chunk: {e}")
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': f'Failed to process audio chunk: {str(e)}'
            }))
    
    async def handle_start_session(self, data):
        """Handle session start"""
        language_code = data.get('language_code', 'hi')
        
        session = await self.create_session(language_code)
        
        await self.send(text_data=json.dumps({
            'type': 'session_started',
            'session_id': self.session_id,
            'language_code': language_code
        }))
    
    async def handle_end_session(self, data):
        """Handle session end"""
        await self.end_session()
        
        await self.send(text_data=json.dumps({
            'type': 'session_ended',
            'session_id': self.session_id
        }))
    
    @database_sync_to_async
    def create_session(self, language_code):
        """Create transcription session in database"""
        session, created = TranscriptionSession.objects.get_or_create(
            session_id=self.session_id,
            defaults={
                'language_code': language_code,
                'is_active': True
            }
        )
        return session
    
    @database_sync_to_async
    def end_session(self):
        """End transcription session in database"""
        try:
            session = TranscriptionSession.objects.get(session_id=self.session_id)
            session.is_active = False
            session.save()
        except TranscriptionSession.DoesNotExist:
            pass
    
    @database_sync_to_async
    def transcribe_audio(self, audio_array, sample_rate, language_code, chunk_number):
        """Transcribe audio using IndicConformer model"""
        try:
            # Get model instance
            model_instance = IndicConformerModel.get_instance()
            
            # Transcribe
            if len(audio_array) == 0:
                transcription = ""
            else:
                transcription = model_instance.transcribe(
                    audio_array, sample_rate, language_code
                )
            
            # Save result to database
            try:
                session = TranscriptionSession.objects.get(session_id=self.session_id)
                TranscriptionResult.objects.create(
                    session=session,
                    chunk_number=chunk_number,
                    transcription_text=transcription
                )
            except TranscriptionSession.DoesNotExist:
                logger.warning(f"Session {self.session_id} not found in database")
            
            return transcription
            
        except Exception as e:
            logger.error(f"Error in transcription: {e}")
            return f"[Transcription error: {str(e)}]"