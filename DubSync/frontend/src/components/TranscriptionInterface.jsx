import React, { useState, useEffect, useRef, useCallback } from 'react'
import { Card, Form, Button, Alert, Badge } from 'react-bootstrap'
import { FaMicrophone, FaStop, FaPlay, FaDownload } from 'react-icons/fa'
import { useAudioRecorder } from '../hooks/useAudioRecorder'
import { apiService } from '../services/apiService'
import { websocketService } from '../services/websocketService'
import { 
  audioToBase64, 
  detectSpeech, 
  normalizeAudio, 
  generateSessionId,
  formatTimestamp 
} from '../utils/audioUtils'

const TranscriptionInterface = ({ isBackendHealthy, onRetryConnection }) => {
  const [languages, setLanguages] = useState([])
  const [selectedLanguage, setSelectedLanguage] = useState('hi')
  const [transcriptions, setTranscriptions] = useState([])
  const [sessionId, setSessionId] = useState(null)
  const [status, setStatus] = useState('ready')
  const [error, setError] = useState(null)
  const [useWebSocket, setUseWebSocket] = useState(false)
  const [chunkNumber, setChunkNumber] = useState(0)
  
  const { isRecording, error: recordingError, startRecording, stopRecording, clearError } = useAudioRecorder()
  const audioBufferRef = useRef([])
  const lastTranscriptionRef = useRef('')

  // Load supported languages on component mount
  useEffect(() => {
    if (isBackendHealthy) {
      loadLanguages()
    }
  }, [isBackendHealthy])

  // Setup WebSocket message handlers
  useEffect(() => {
    const handleTranscriptionResult = (data) => {
      if (data.transcription && data.transcription.trim()) {
        addTranscription(data.transcription, data.chunk_number)
      }
    }

    const handleError = (data) => {
      setError(data.message)
      setStatus('error')
    }

    const handleSessionStarted = (data) => {
      console.log('Session started:', data)
      setStatus('recording')
    }

    const handleSessionEnded = (data) => {
      console.log('Session ended:', data)
      setStatus('ready')
    }

    websocketService.onMessage('transcription_result', handleTranscriptionResult)
    websocketService.onMessage('error', handleError)
    websocketService.onMessage('session_started', handleSessionStarted)
    websocketService.onMessage('session_ended', handleSessionEnded)

    return () => {
      websocketService.offMessage('transcription_result', handleTranscriptionResult)
      websocketService.offMessage('error', handleError)
      websocketService.offMessage('session_started', handleSessionStarted)
      websocketService.offMessage('session_ended', handleSessionEnded)
    }
  }, [])

  const loadLanguages = async () => {
    try {
      const languageList = await apiService.getSupportedLanguages()
      setLanguages(languageList)
    } catch (error) {
      console.error('Failed to load languages:', error)
      setError('Failed to load supported languages')
    }
  }

  const addTranscription = useCallback((text, chunkNum) => {
    if (text && text !== lastTranscriptionRef.current) {
      const timestamp = new Date().toISOString()
      setTranscriptions(prev => [...prev, {
        id: Date.now() + Math.random(),
        text: text.trim(),
        timestamp,
        chunkNumber: chunkNum || 0
      }])
      lastTranscriptionRef.current = text
    }
  }, [])

  const handleAudioData = useCallback(async (audioData) => {
    if (!sessionId || !isRecording) return

    try {
      // Normalize audio
      const normalizedAudio = normalizeAudio(audioData)
      
      // Check if audio contains speech
      if (!detectSpeech(normalizedAudio, 0.01)) {
        return // Skip silent chunks
      }

      // Convert to base64
      const base64Audio = audioToBase64(normalizedAudio)
      
      if (useWebSocket && websocketService.isConnected) {
        // Send via WebSocket
        websocketService.sendAudioChunk(
          base64Audio,
          selectedLanguage,
          chunkNumber,
          16000
        )
      } else {
        // Send via HTTP API
        const result = await apiService.transcribeAudioChunk(
          base64Audio,
          sessionId,
          selectedLanguage,
          chunkNumber,
          16000
        )
        
        if (result.transcription && result.transcription.trim()) {
          addTranscription(result.transcription, result.chunk_number)
        }
      }
      
      setChunkNumber(prev => prev + 1)
      
    } catch (error) {
      console.error('Error processing audio data:', error)
      setError(`Audio processing error: ${error.message}`)
    }
  }, [sessionId, isRecording, selectedLanguage, chunkNumber, useWebSocket, addTranscription])

  const handleStartRecording = async () => {
    try {
      setError(null)
      clearError()
      
      // Create new session
      const newSessionId = generateSessionId()
      setSessionId(newSessionId)
      setChunkNumber(0)
      setTranscriptions([])
      lastTranscriptionRef.current = ''
      
      if (useWebSocket) {
        // Connect WebSocket
        await websocketService.connect(newSessionId)
        websocketService.startSession(selectedLanguage)
      } else {
        // Create session via API
        await apiService.createSession(selectedLanguage)
      }
      
      setStatus('recording')
      
      // Start audio recording
      await startRecording(handleAudioData)
      
    } catch (error) {
      console.error('Error starting recording:', error)
      setError(`Failed to start recording: ${error.message}`)
      setStatus('error')
    }
  }

  const handleStopRecording = async () => {
    try {
      stopRecording()
      
      if (useWebSocket && websocketService.isConnected) {
        websocketService.endSession()
        websocketService.disconnect()
      } else if (sessionId) {
        await apiService.endSession(sessionId)
      }
      
      setStatus('ready')
      
    } catch (error) {
      console.error('Error stopping recording:', error)
      setError(`Failed to stop recording: ${error.message}`)
    }
  }

  const handleClearTranscriptions = () => {
    setTranscriptions([])
    lastTranscriptionRef.current = ''
  }

  const handleDownloadTranscriptions = () => {
    const text = transcriptions.map(t => 
      `[${formatTimestamp(t.timestamp)}] ${t.text}`
    ).join('\n')
    
    const blob = new Blob([text], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `transcription_${new Date().toISOString().split('T')[0]}.txt`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  const getStatusBadge = () => {
    switch (status) {
      case 'recording':
        return <Badge bg="danger" className="status-indicator">
          <div className="recording-pulse"></div>
          Recording
        </Badge>
      case 'error':
        return <Badge bg="danger" className="status-indicator">Error</Badge>
      default:
        return <Badge bg="success" className="status-indicator">Ready</Badge>
    }
  }

  if (!isBackendHealthy) {
    return (
      <Card className="transcription-interface">
        <Card.Body className="text-center">
          <h5>Backend Service Unavailable</h5>
          <p>Please ensure the Django backend is running and try again.</p>
          <Button variant="primary" onClick={onRetryConnection}>
            Retry Connection
          </Button>
        </Card.Body>
      </Card>
    )
  }

  return (
    <Card className="transcription-interface">
      <Card.Body>
        <div className="text-center mb-4">
          {getStatusBadge()}
        </div>

        {error && (
          <Alert variant="danger" dismissible onClose={() => setError(null)}>
            {error}
          </Alert>
        )}

        {recordingError && (
          <Alert variant="warning" dismissible onClose={clearError}>
            Recording Error: {recordingError}
          </Alert>
        )}

        <Form className="mb-4">
          <Form.Group className="language-selector">
            <Form.Label><strong>Select Language:</strong></Form.Label>
            <Form.Select
              value={selectedLanguage}
              onChange={(e) => setSelectedLanguage(e.target.value)}
              disabled={isRecording}
            >
              {languages.map(lang => (
                <option key={lang.code} value={lang.code}>
                  {lang.name} ({lang.code})
                </option>
              ))}
            </Form.Select>
          </Form.Group>

          <Form.Group className="mb-3">
            <Form.Check
              type="checkbox"
              label="Use WebSocket (Real-time)"
              checked={useWebSocket}
              onChange={(e) => setUseWebSocket(e.target.checked)}
              disabled={isRecording}
            />
          </Form.Group>
        </Form>

        <div className="control-buttons">
          {!isRecording ? (
            <Button
              variant="success"
              size="lg"
              onClick={handleStartRecording}
              disabled={!isBackendHealthy || status === 'error'}
              className="btn-record"
            >
              <FaMicrophone className="me-2" />
              Start Recording
            </Button>
          ) : (
            <Button
              variant="danger"
              size="lg"
              onClick={handleStopRecording}
              className="btn-stop"
            >
              <FaStop className="me-2" />
              Stop Recording
            </Button>
          )}
        </div>

        <div className="transcription-output">
          <div className="d-flex justify-content-between align-items-center mb-3">
            <h6 className="mb-0">Live Transcription:</h6>
            <div>
              <Button
                variant="outline-secondary"
                size="sm"
                onClick={handleClearTranscriptions}
                disabled={transcriptions.length === 0}
                className="me-2"
              >
                Clear
              </Button>
              <Button
                variant="outline-primary"
                size="sm"
                onClick={handleDownloadTranscriptions}
                disabled={transcriptions.length === 0}
              >
                <FaDownload className="me-1" />
                Download
              </Button>
            </div>
          </div>

          {transcriptions.length === 0 ? (
            <div className="text-muted text-center py-4">
              {isRecording ? 'Listening for speech...' : 'Transcriptions will appear here'}
            </div>
          ) : (
            <div>
              {transcriptions.map((transcription) => (
                <div key={transcription.id} className="transcription-line">
                  <small className="text-muted">
                    [{formatTimestamp(transcription.timestamp)}]
                  </small>
                  <div>{transcription.text}</div>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="mt-3 text-center">
          <small className="text-muted">
            Session ID: {sessionId || 'Not started'} | 
            Chunks processed: {chunkNumber} |
            Connection: {useWebSocket ? 'WebSocket' : 'HTTP API'}
          </small>
        </div>
      </Card.Body>
    </Card>
  )
}

export default TranscriptionInterface