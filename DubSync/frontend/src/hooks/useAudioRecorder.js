import { useState, useRef, useCallback } from 'react'

export const useAudioRecorder = () => {
  const [isRecording, setIsRecording] = useState(false)
  const [error, setError] = useState(null)
  const mediaRecorderRef = useRef(null)
  const streamRef = useRef(null)
  const audioContextRef = useRef(null)
  const processorRef = useRef(null)
  const onAudioDataRef = useRef(null)

  const startRecording = useCallback(async (onAudioData) => {
    try {
      setError(null)
      onAudioDataRef.current = onAudioData

      // Request microphone access
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: {
          sampleRate: 16000,
          channelCount: 1,
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true,
        }
      })

      streamRef.current = stream

      // Create audio context for real-time processing
      audioContextRef.current = new (window.AudioContext || window.webkitAudioContext)({
        sampleRate: 16000
      })

      const source = audioContextRef.current.createMediaStreamSource(stream)
      
      // Create script processor for real-time audio chunks
      const bufferSize = 4096
      processorRef.current = audioContextRef.current.createScriptProcessor(bufferSize, 1, 1)
      
      processorRef.current.onaudioprocess = (event) => {
        if (isRecording && onAudioDataRef.current) {
          const inputBuffer = event.inputBuffer
          const inputData = inputBuffer.getChannelData(0)
          
          // Convert to Float32Array and send to callback
          const audioData = new Float32Array(inputData)
          onAudioDataRef.current(audioData)
        }
      }

      source.connect(processorRef.current)
      processorRef.current.connect(audioContextRef.current.destination)

      setIsRecording(true)
      console.log('Recording started')

    } catch (err) {
      console.error('Error starting recording:', err)
      setError(err.message)
      throw err
    }
  }, [isRecording])

  const stopRecording = useCallback(() => {
    try {
      setIsRecording(false)

      // Stop audio processing
      if (processorRef.current) {
        processorRef.current.disconnect()
        processorRef.current = null
      }

      // Close audio context
      if (audioContextRef.current) {
        audioContextRef.current.close()
        audioContextRef.current = null
      }

      // Stop media stream
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(track => track.stop())
        streamRef.current = null
      }

      onAudioDataRef.current = null
      console.log('Recording stopped')

    } catch (err) {
      console.error('Error stopping recording:', err)
      setError(err.message)
    }
  }, [])

  const clearError = useCallback(() => {
    setError(null)
  }, [])

  return {
    isRecording,
    error,
    startRecording,
    stopRecording,
    clearError
  }
}