import React, { useState, useEffect } from 'react'
import { Container, Row, Col, Alert } from 'react-bootstrap'
import TranscriptionInterface from './components/TranscriptionInterface'
import { apiService } from './services/apiService'
import './App.css'

function App() {
  const [isBackendHealthy, setIsBackendHealthy] = useState(null)
  const [healthError, setHealthError] = useState(null)

  useEffect(() => {
    checkBackendHealth()
  }, [])

  const checkBackendHealth = async () => {
    try {
      const health = await apiService.checkHealth()
      setIsBackendHealthy(true)
      setHealthError(null)
      console.log('Backend health:', health)
    } catch (error) {
      setIsBackendHealthy(false)
      setHealthError(error.message)
      console.error('Backend health check failed:', error)
    }
  }

  return (
    <div className="app-container">
      <Container fluid>
        <Row className="justify-content-center">
          <Col xs={12} lg={10} xl={8}>
            <div className="text-center mb-4">
              <h1 className="header-title display-4 fw-bold">
                🎙️ DubSync
              </h1>
              <p className="header-subtitle lead">
                Real-Time Speech Transcription for Indian Languages
              </p>
              <p className="header-subtitle">
                Powered by AI4Bharat IndicConformer • Supporting 22 Indian Languages
              </p>
            </div>

            {isBackendHealthy === false && (
              <Alert variant="danger" className="mb-4">
                <Alert.Heading>Backend Connection Error</Alert.Heading>
                <p>
                  Unable to connect to the transcription service. Please ensure the backend server is running.
                </p>
                <p className="mb-0">
                  <strong>Error:</strong> {healthError}
                </p>
                <hr />
                <div className="d-flex justify-content-end">
                  <button 
                    className="btn btn-outline-danger"
                    onClick={checkBackendHealth}
                  >
                    Retry Connection
                  </button>
                </div>
              </Alert>
            )}

            {isBackendHealthy === null && (
              <Alert variant="info" className="mb-4">
                <div className="d-flex align-items-center">
                  <div className="loading-spinner me-3"></div>
                  Checking backend connection...
                </div>
              </Alert>
            )}

            <TranscriptionInterface 
              isBackendHealthy={isBackendHealthy}
              onRetryConnection={checkBackendHealth}
            />
          </Col>
        </Row>
      </Container>
    </div>
  )
}

export default App