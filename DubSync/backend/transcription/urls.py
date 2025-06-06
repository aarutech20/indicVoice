from django.urls import path
from . import views

urlpatterns = [
    path('health/', views.health_check, name='health_check'),
    path('languages/', views.get_supported_languages, name='supported_languages'),
    path('transcribe/', views.TranscriptionView.as_view(), name='transcribe'),
    path('session/create/', views.create_session, name='create_session'),
    path('session/<str:session_id>/end/', views.end_session, name='end_session'),
    path('session/<str:session_id>/results/', views.get_session_results, name='session_results'),
]