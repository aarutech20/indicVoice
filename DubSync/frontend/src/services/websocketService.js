class WebSocketService {
  constructor() {
    this.ws = null
    this.sessionId = null
    this.isConnected = false
    this.messageHandlers = new Map()
    this.reconnectAttempts = 0
    this.maxReconnectAttempts = 5
    this.reconnectDelay = 1000
  }

  connect(sessionId) {
    return new Promise((resolve, reject) => {
      try {
        this.sessionId = sessionId
        const wsUrl = `ws://localhost:8000/ws/transcription/${sessionId}/`
        
        console.log(`Connecting to WebSocket: ${wsUrl}`)
        this.ws = new WebSocket(wsUrl)

        this.ws.onopen = () => {
          console.log('WebSocket connected')
          this.isConnected = true
          this.reconnectAttempts = 0
          resolve()
        }

        this.ws.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data)
            this.handleMessage(data)
          } catch (error) {
            console.error('Error parsing WebSocket message:', error)
          }
        }

        this.ws.onclose = (event) => {
          console.log('WebSocket disconnected:', event.code, event.reason)
          this.isConnected = false
          
          if (event.code !== 1000 && this.reconnectAttempts < this.maxReconnectAttempts) {
            this.attemptReconnect()
          }
        }

        this.ws.onerror = (error) => {
          console.error('WebSocket error:', error)
          reject(error)
        }

      } catch (error) {
        console.error('Failed to create WebSocket connection:', error)
        reject(error)
      }
    })
  }

  attemptReconnect() {
    this.reconnectAttempts++
    console.log(`Attempting to reconnect (${this.reconnectAttempts}/${this.maxReconnectAttempts})...`)
    
    setTimeout(() => {
      if (this.sessionId) {
        this.connect(this.sessionId).catch(error => {
          console.error('Reconnection failed:', error)
        })
      }
    }, this.reconnectDelay * this.reconnectAttempts)
  }

  disconnect() {
    if (this.ws) {
      this.ws.close(1000, 'Client disconnecting')
      this.ws = null
      this.isConnected = false
      this.sessionId = null
    }
  }

  sendMessage(message) {
    if (this.ws && this.isConnected) {
      this.ws.send(JSON.stringify(message))
    } else {
      console.error('WebSocket not connected')
      throw new Error('WebSocket not connected')
    }
  }

  sendAudioChunk(audioData, languageCode, chunkNumber, sampleRate = 16000) {
    this.sendMessage({
      type: 'audio_chunk',
      audio_data: audioData,
      language_code: languageCode,
      chunk_number: chunkNumber,
      sample_rate: sampleRate
    })
  }

  startSession(languageCode) {
    this.sendMessage({
      type: 'start_session',
      language_code: languageCode
    })
  }

  endSession() {
    this.sendMessage({
      type: 'end_session'
    })
  }

  handleMessage(data) {
    const { type } = data
    
    if (this.messageHandlers.has(type)) {
      const handlers = this.messageHandlers.get(type)
      handlers.forEach(handler => {
        try {
          handler(data)
        } catch (error) {
          console.error(`Error in message handler for ${type}:`, error)
        }
      })
    } else {
      console.log('Unhandled message type:', type, data)
    }
  }

  onMessage(type, handler) {
    if (!this.messageHandlers.has(type)) {
      this.messageHandlers.set(type, [])
    }
    this.messageHandlers.get(type).push(handler)
  }

  offMessage(type, handler) {
    if (this.messageHandlers.has(type)) {
      const handlers = this.messageHandlers.get(type)
      const index = handlers.indexOf(handler)
      if (index > -1) {
        handlers.splice(index, 1)
      }
    }
  }

  clearMessageHandlers() {
    this.messageHandlers.clear()
  }
}

export const websocketService = new WebSocketService()