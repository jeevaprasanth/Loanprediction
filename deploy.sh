#!/bin/bash

# Loan AI System Deployment Script
echo "🚀 Deploying Loan AI System..."

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

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p data models logs

# Set environment variables
echo "🔧 Setting up environment..."
export FLASK_ENV=production
export DATABASE_TYPE=sqlite

# Build and run containers
echo "🏗️ Building Docker containers..."
docker-compose build

echo "🚀 Starting containers..."
docker-compose up -d

# Wait for the application to start
echo "⏳ Waiting for application to start..."
sleep 10

# Check if the application is running
if curl -f http://localhost:5000/health > /dev/null 2>&1; then
    echo "✅ Loan AI System is running successfully!"
    echo "🌐 Access your application at: http://localhost:5000"
    echo "📊 Check the health status at: http://localhost:5000/health"
    echo ""
    echo "🔍 To view logs: docker-compose logs -f"
    echo "🛑 To stop: docker-compose down"
    echo "🔄 To restart: docker-compose restart"
else
    echo "❌ Application failed to start. Check logs with: docker-compose logs"
    exit 1
fi
