import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'

class ApiService {
  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    })

    // Request interceptor
    this.client.interceptors.request.use(
      (config) => {
        console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`)
        return config
      },
      (error) => {
        console.error('API Request Error:', error)
        return Promise.reject(error)
      }
    )

    // Response interceptor
    this.client.interceptors.response.use(
      (response) => {
        console.log(`API Response: ${response.status} ${response.config.url}`)
        return response
      },
      (error) => {
        console.error('API Response Error:', error.response?.data || error.message)
        return Promise.reject(error)
      }
    )
  }

  async checkHealth() {
    try {
      const response = await this.client.get('/health/')
      return response.data
    } catch (error) {
      throw new Error(`Health check failed: ${error.message}`)
    }
  }

  async getSupportedLanguages() {
    try {
      const response = await this.client.get('/languages/')
      return response.data.languages
    } catch (error) {
      throw new Error(`Failed to get languages: ${error.message}`)
    }
  }

  async createSession(languageCode) {
    try {
      const response = await this.client.post('/session/create/', {
        language_code: languageCode
      })
      return response.data
    } catch (error) {
      throw new Error(`Failed to create session: ${error.message}`)
    }
  }

  async endSession(sessionId) {
    try {
      const response = await this.client.post(`/session/${sessionId}/end/`)
      return response.data
    } catch (error) {
      throw new Error(`Failed to end session: ${error.message}`)
    }
  }

  async getSessionResults(sessionId) {
    try {
      const response = await this.client.get(`/session/${sessionId}/results/`)
      return response.data
    } catch (error) {
      throw new Error(`Failed to get session results: ${error.message}`)
    }
  }

  async transcribeAudioChunk(audioData, sessionId, languageCode, chunkNumber, sampleRate = 16000) {
    try {
      const response = await this.client.post('/transcribe/', {
        audio_data: audioData,
        session_id: sessionId,
        language_code: languageCode,
        chunk_number: chunkNumber,
        sample_rate: sampleRate
      })
      return response.data
    } catch (error) {
      throw new Error(`Transcription failed: ${error.message}`)
    }
  }
}

export const apiService = new ApiService()