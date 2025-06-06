from django.contrib import admin
from .models import TranscriptionSession, TranscriptionResult

@admin.register(TranscriptionSession)
class TranscriptionSessionAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'language_code', 'is_active', 'created_at', 'updated_at']
    list_filter = ['language_code', 'is_active', 'created_at']
    search_fields = ['session_id']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(TranscriptionResult)
class TranscriptionResultAdmin(admin.ModelAdmin):
    list_display = ['session', 'chunk_number', 'transcription_text_preview', 'timestamp']
    list_filter = ['session__language_code', 'timestamp']
    search_fields = ['transcription_text', 'session__session_id']
    readonly_fields = ['timestamp']
    
    def transcription_text_preview(self, obj):
        return obj.transcription_text[:100] + "..." if len(obj.transcription_text) > 100 else obj.transcription_text
    transcription_text_preview.short_description = "Transcription Preview"