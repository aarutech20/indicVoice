#!/bin/bash

# DubSync Test Setup Script
# This script tests the project structure and basic functionality

set -e

echo "🧪 DubSync Test Setup Script"
echo "============================="

# Test project structure
echo "📁 Testing project structure..."

required_files=(
    "README.md"
    "docker-compose.yml"
    "docker-compose.cpu.yml"
    ".gitignore"
    "LICENSE"
    "Makefile"
    "backend/requirements.txt"
    "backend/manage.py"
    "backend/Dockerfile"
    "backend/dubsync_backend/settings.py"
    "backend/transcription/models.py"
    "backend/transcription/views.py"
    "frontend/package.json"
    "frontend/vite.config.js"
    "frontend/Dockerfile"
    "frontend/src/App.jsx"
    "frontend/src/main.jsx"
    "frontend/src/components/TranscriptionInterface.jsx"
    "frontend/src/services/apiService.js"
    "frontend/src/hooks/useAudioRecorder.js"
)

missing_files=()
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        missing_files+=("$file")
    fi
done

if [ ${#missing_files[@]} -eq 0 ]; then
    echo "✅ All required files present"
else
    echo "❌ Missing files:"
    for file in "${missing_files[@]}"; do
        echo "   - $file"
    done
    exit 1
fi

# Test Docker Compose syntax (if docker-compose is available)
echo "🐳 Testing Docker Compose configuration..."
if command -v docker-compose &> /dev/null; then
    if docker-compose -f docker-compose.yml config > /dev/null 2>&1; then
        echo "✅ docker-compose.yml is valid"
    else
        echo "❌ docker-compose.yml has syntax errors"
        exit 1
    fi

    if docker-compose -f docker-compose.cpu.yml config > /dev/null 2>&1; then
        echo "✅ docker-compose.cpu.yml is valid"
    else
        echo "❌ docker-compose.cpu.yml has syntax errors"
        exit 1
    fi
else
    echo "⚠️ docker-compose not found, skipping validation"
fi

# Test Python syntax
echo "🐍 Testing Python syntax..."
python_files=$(find backend -name "*.py" -type f)
for file in $python_files; do
    if ! python -m py_compile "$file" 2>/dev/null; then
        echo "❌ Python syntax error in $file"
        exit 1
    fi
done
echo "✅ All Python files have valid syntax"

# Test package.json
echo "📦 Testing package.json..."
if [ -f "frontend/package.json" ]; then
    if node -e "JSON.parse(require('fs').readFileSync('frontend/package.json', 'utf8'))" 2>/dev/null; then
        echo "✅ package.json is valid JSON"
    else
        echo "❌ package.json has invalid JSON syntax"
        exit 1
    fi
fi

# Test environment files
echo "🔧 Testing environment configuration..."
if [ -f ".env.example" ]; then
    echo "✅ .env.example found"
else
    echo "❌ .env.example not found"
    exit 1
fi

# Test documentation
echo "📚 Testing documentation..."
if grep -q "DubSync" README.md && grep -q "installation" README.md; then
    echo "✅ README.md contains required sections"
else
    echo "❌ README.md missing required content"
    exit 1
fi

echo ""
echo "🎉 All tests passed!"
echo ""
echo "🚀 Your DubSync project is ready for deployment!"
echo ""
echo "Next steps:"
echo "1. Run: ./scripts/setup.sh"
echo "2. Or manually: docker-compose up --build"
echo "3. Access: http://localhost:3000"
echo ""
echo "For development:"
echo "1. Backend: cd backend && pip install -r requirements.txt && python manage.py runserver"
echo "2. Frontend: cd frontend && npm install && npm run dev"