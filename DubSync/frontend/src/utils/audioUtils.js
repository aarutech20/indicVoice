/**
 * Convert Float32Array audio data to base64 string
 */
export const audioToBase64 = (audioData) => {
  try {
    // Convert Float32Array to ArrayBuffer
    const buffer = audioData.buffer.slice(
      audioData.byteOffset,
      audioData.byteOffset + audioData.byteLength
    )
    
    // Convert ArrayBuffer to base64
    const bytes = new Uint8Array(buffer)
    let binary = ''
    for (let i = 0; i < bytes.byteLength; i++) {
      binary += String.fromCharCode(bytes[i])
    }
    
    return btoa(binary)
  } catch (error) {
    console.error('Error converting audio to base64:', error)
    throw error
  }
}

/**
 * Resample audio data to target sample rate
 */
export const resampleAudio = (audioData, originalSampleRate, targetSampleRate) => {
  if (originalSampleRate === targetSampleRate) {
    return audioData
  }

  const ratio = originalSampleRate / targetSampleRate
  const newLength = Math.round(audioData.length / ratio)
  const result = new Float32Array(newLength)

  for (let i = 0; i < newLength; i++) {
    const index = i * ratio
    const indexFloor = Math.floor(index)
    const indexCeil = Math.min(indexFloor + 1, audioData.length - 1)
    const fraction = index - indexFloor

    result[i] = audioData[indexFloor] * (1 - fraction) + audioData[indexCeil] * fraction
  }

  return result
}

/**
 * Apply simple noise gate to audio data
 */
export const applyNoiseGate = (audioData, threshold = 0.01) => {
  const result = new Float32Array(audioData.length)
  
  for (let i = 0; i < audioData.length; i++) {
    result[i] = Math.abs(audioData[i]) > threshold ? audioData[i] : 0
  }
  
  return result
}

/**
 * Calculate RMS (Root Mean Square) of audio data
 */
export const calculateRMS = (audioData) => {
  let sum = 0
  for (let i = 0; i < audioData.length; i++) {
    sum += audioData[i] * audioData[i]
  }
  return Math.sqrt(sum / audioData.length)
}

/**
 * Detect if audio chunk contains speech (simple volume-based detection)
 */
export const detectSpeech = (audioData, threshold = 0.02) => {
  const rms = calculateRMS(audioData)
  return rms > threshold
}

/**
 * Normalize audio data to prevent clipping
 */
export const normalizeAudio = (audioData) => {
  const max = Math.max(...audioData.map(Math.abs))
  if (max === 0) return audioData
  
  const result = new Float32Array(audioData.length)
  const scale = 0.95 / max // Leave some headroom
  
  for (let i = 0; i < audioData.length; i++) {
    result[i] = audioData[i] * scale
  }
  
  return result
}

/**
 * Chunk audio data into smaller segments
 */
export const chunkAudioData = (audioData, chunkSize) => {
  const chunks = []
  for (let i = 0; i < audioData.length; i += chunkSize) {
    chunks.push(audioData.slice(i, i + chunkSize))
  }
  return chunks
}

/**
 * Generate a unique session ID
 */
export const generateSessionId = () => {
  return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
}

/**
 * Format timestamp for display
 */
export const formatTimestamp = (timestamp) => {
  const date = new Date(timestamp)
  return date.toLocaleTimeString('en-US', {
    hour12: false,
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}