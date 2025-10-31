#!/bin/bash

# Merlin Development Server Startup Script

echo "🧙‍♂️ Starting Merlin Development Environment..."

# Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: Please run this script from the merlin root directory"
    exit 1
fi

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "🔍 Checking prerequisites..."

if ! command_exists python3; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

if ! command_exists npm; then
    echo "❌ Node.js and npm are required but not installed"
    exit 1
fi

# Install Python dependencies if needed
if [ ! -d ".venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv .venv
fi

echo "🐍 Activating virtual environment and installing dependencies..."
source .venv/bin/activate
pip install -r requirements.txt

# Install frontend dependencies if needed
if [ ! -d "frontend/node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    cd frontend
    npm install
    cd ..
fi

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found. Creating template..."
    cat > .env << EOL
# AI Configuration
GROQ_API_KEY=your_groq_api_key_here

# Django Settings
DEBUG=True
SECRET_KEY=django-insecure-development-key-change-in-production
EOL
    echo "📝 Please edit .env file with your actual API keys"
fi

# Run database migrations
echo "🗄️  Running database migrations..."
cd src
python manage.py migrate
cd ..

echo "🚀 Starting development servers..."

# Function to handle cleanup
cleanup() {
    echo "🛑 Shutting down servers..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Start backend server
echo "🔧 Starting Django backend on http://localhost:8000..."
cd src
python manage.py runserver &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
sleep 3

# Start frontend server
echo "⚛️  Starting React frontend on http://localhost:3000..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ Development environment is ready!"
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend: http://localhost:8000"
echo "👑 Admin: http://localhost:8000/admin"
echo ""
echo "Press Ctrl+C to stop all servers"

# Wait for background processes
wait $BACKEND_PID $FRONTEND_PID
