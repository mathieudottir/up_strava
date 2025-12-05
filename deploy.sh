#!/bin/bash

# Strava Gamification Platform - Deployment Script
# Usage: ./deploy.sh

set -e

echo "🚀 Starting deployment of Strava Gamification Platform..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "Please create .env file from .env.example and configure it."
    exit 1
fi

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker is not running!"
    exit 1
fi

# Pull latest changes (if in git repo)
if [ -d .git ]; then
    echo "📥 Pulling latest changes..."
    git pull
fi

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose down

# Build images
echo "🔨 Building Docker images..."
docker-compose build --no-cache

# Start services
echo "▶️  Starting services..."
docker-compose up -d

# Wait for services to be healthy
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check service status
echo "📊 Service status:"
docker-compose ps

# Show logs
echo ""
echo "✅ Deployment completed!"
echo ""
echo "Services are running:"
echo "  - Frontend: http://localhost:3000"
echo "  - Backend API: http://localhost:8000"
echo "  - API Docs: http://localhost:8000/docs"
echo ""
echo "To view logs: docker-compose logs -f"
echo "To stop services: docker-compose down"
echo ""

# Optional: Show initial logs
read -p "Show logs? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    docker-compose logs -f
fi
