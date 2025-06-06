#!/bin/bash

# DubSync Setup Script
# This script sets up the development environment

set -e

echo "🎙️ DubSync Setup Script"
echo "========================"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Please run this script from the DubSync root directory."
    exit 1
fi

echo "✅ Prerequisites check passed"

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created. Please review and modify if needed."
fi

# Check for NVIDIA GPU
if command -v nvidia-smi &> /dev/null; then
    echo "🚀 NVIDIA GPU detected. Using GPU-enabled configuration."
    COMPOSE_FILE="docker-compose.yml"
else
    echo "💻 No NVIDIA GPU detected. Using CPU-only configuration."
    COMPOSE_FILE="docker-compose.cpu.yml"
fi

echo "🔨 Building Docker containers..."
docker-compose -f $COMPOSE_FILE build

echo "🚀 Starting services..."
docker-compose -f $COMPOSE_FILE up -d

echo "⏳ Waiting for services to start..."
sleep 30

# Health check
echo "🔍 Checking service health..."
if curl -f http://localhost:8000/api/health/ &> /dev/null; then
    echo "✅ Backend is healthy"
else
    echo "⚠️ Backend health check failed"
fi

if curl -f http://localhost:3000/ &> /dev/null; then
    echo "✅ Frontend is healthy"
else
    echo "⚠️ Frontend health check failed"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📱 Access your application:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000/api"
echo "   Admin Panel: http://localhost:8000/admin"
echo ""
echo "🔧 Useful commands:"
echo "   View logs: docker-compose -f $COMPOSE_FILE logs -f"
echo "   Stop services: docker-compose -f $COMPOSE_FILE down"
echo "   Restart: docker-compose -f $COMPOSE_FILE restart"
echo ""
echo "📚 For more information, see README.md"