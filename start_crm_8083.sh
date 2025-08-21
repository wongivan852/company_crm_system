#!/bin/bash

# Start CRM System on port 8083 with Docker Compose
# This script consolidates all necessary services

set -e

echo "====================================="
echo "  CRM System - Docker Deployment"
echo "  Port: 8083"
echo "====================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Error: docker-compose is not installed. Please install docker-compose and try again."
    exit 1
fi

# Change to script directory
cd "$(dirname "$0")"

echo "📁 Working directory: $(pwd)"
echo "🔍 Checking configuration..."

# Verify essential files exist
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Error: docker-compose.yml not found!"
    exit 1
fi

if [ ! -f "Dockerfile" ]; then
    echo "❌ Error: Dockerfile not found!"
    exit 1
fi

if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: requirements.txt not found!"
    exit 1
fi

# Create necessary directories
echo "📂 Creating necessary directories..."
mkdir -p logs data/datasets data/backups media static

# Check if datasets exist
echo "📊 Checking datasets..."
if [ -d "data/datasets" ] && [ "$(ls -A data/datasets 2>/dev/null)" ]; then
    echo "✅ Datasets found in data/datasets/"
    ls -la data/datasets/
else
    echo "⚠️  Warning: No datasets found in data/datasets/"
fi

# Stop any existing containers
echo "🛑 Stopping existing containers..."
docker-compose down --remove-orphans 2>/dev/null || true

# Clean up old images if requested
if [ "$1" = "--clean" ]; then
    echo "🧹 Cleaning old images..."
    docker-compose down --rmi all --volumes --remove-orphans
    docker system prune -f
fi

# Build and start services
echo "🏗️  Building and starting services..."
echo "This may take a few minutes for the first build..."

# Build with no cache if --rebuild flag is passed
if [ "$1" = "--rebuild" ]; then
    docker-compose build --no-cache
else
    docker-compose build
fi

# Start services in background
docker-compose up -d

echo "⏳ Waiting for services to be ready..."

# Wait for database to be ready
echo "🗄️  Waiting for database..."
timeout=60
counter=0
while ! docker-compose exec -T db pg_isready -U crm_user -d crm_db; do
    if [ $counter -ge $timeout ]; then
        echo "❌ Timeout waiting for database"
        docker-compose logs db
        exit 1
    fi
    echo "Waiting for database... ($counter/$timeout)"
    sleep 2
    counter=$((counter + 2))
done

# Wait for web service to be ready
echo "🌐 Waiting for web service..."
timeout=120
counter=0
while ! curl -f http://localhost:8083/ > /dev/null 2>&1; do
    if [ $counter -ge $timeout ]; then
        echo "❌ Timeout waiting for web service"
        echo "📋 Web service logs:"
        docker-compose logs web
        exit 1
    fi
    echo "Waiting for web service... ($counter/$timeout)"
    sleep 5
    counter=$((counter + 5))
done

echo ""
echo "✅ CRM System is now running!"
echo ""
echo "📱 Access URLs:"
echo "   🏠 Main Application: http://localhost:8083/"
echo "   ⚙️  Admin Panel:      http://localhost:8083/admin/"
echo "   📊 API Docs:         http://localhost:8083/api/"
echo ""
echo "🔐 Default Admin Credentials:"
echo "   Username: admin"
echo "   Password: admin123"
echo "   (Change these in production!)"
echo ""
echo "📊 Services Status:"
docker-compose ps

echo ""
echo "📋 Useful Commands:"
echo "   View logs:       docker-compose logs -f"
echo "   Stop services:   docker-compose down"
echo "   Restart:         docker-compose restart"
echo "   Shell access:    docker-compose exec web sh"
echo ""
echo "🎉 Setup complete! Your CRM system is ready to use."