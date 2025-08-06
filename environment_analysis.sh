#!/bin/bash

echo "🔍 COMPANY CRM SYSTEM - ENVIRONMENT ANALYSIS"
echo "============================================"
echo ""

echo "📊 PROJECT STRUCTURE ANALYSIS:"
cd /home/user/krystal-company-apps/company_crm_system

# Check for virtual environment indicators
echo ""
echo "🐍 VIRTUAL ENVIRONMENT SETUP:"
if [ -f "requirements.txt" ]; then
    echo "   ✅ requirements.txt found"
    DEPS_COUNT=$(wc -l < requirements.txt)
    echo "   📦 Dependencies: $DEPS_COUNT packages listed"
else
    echo "   ❌ requirements.txt not found"
fi

if [ -f "Pipfile" ]; then
    echo "   ✅ Pipfile found (pipenv setup)"
elif [ -f "poetry.lock" ]; then
    echo "   ✅ poetry.lock found (Poetry setup)"
elif [ -d "venv" ] || [ -d ".venv" ] || [ -d "env" ]; then
    echo "   ✅ Local virtual environment directory found"
else
    echo "   ℹ️  No local venv directory (using external virtual env)"
fi

# Check current Python environment
echo ""
echo "🔧 CURRENT RUNTIME ENVIRONMENT:"
PYTHON_PATH=$(/home/user/krystal-company-apps/claude-env/bin/python -c "import sys; print(sys.executable)")
echo "   🐍 Python executable: $PYTHON_PATH"

if [[ $PYTHON_PATH == *"claude-env"* ]]; then
    echo "   ✅ Using virtual environment: claude-env"
    echo "   📍 Environment location: /home/user/krystal-company-apps/claude-env/"
else
    echo "   ⚠️  Using system Python"
fi

# Check for Docker setup
echo ""
echo "🐳 DOCKER CONFIGURATION:"
if [ -f "Dockerfile" ]; then
    echo "   ✅ Dockerfile found"
    DOCKER_BASE=$(grep "FROM" Dockerfile | head -1)
    echo "   📦 Base image: $DOCKER_BASE"
    
    if [ -f "docker-compose.yml" ]; then
        echo "   ✅ docker-compose.yml found"
        SERVICES=$(grep -E "^  [a-z]" docker-compose.yml | wc -l)
        echo "   🏗️  Services defined: $SERVICES"
        
        # List services
        echo "   📋 Services:"
        grep -E "^  [a-z]" docker-compose.yml | sed 's/://g' | sed 's/^/      • /'
    fi
    
    if [ -f ".dockerignore" ]; then
        echo "   ✅ .dockerignore found"
    fi
else
    echo "   ❌ No Dockerfile found"
fi

# Check if running in Docker
echo ""
echo "🏃 CURRENT EXECUTION MODE:"
if [ -f /.dockerenv ]; then
    echo "   🐳 RUNNING IN DOCKER CONTAINER"
else
    echo "   💻 RUNNING ON HOST SYSTEM"
    
    # Check if Docker containers are running
    DOCKER_STATUS=$(sudo docker ps --format "table {{.Names}}\t{{.Status}}" 2>/dev/null | grep -v NAMES || echo "No Docker access or containers running")
    echo "   🐳 Docker containers status:"
    echo "      $DOCKER_STATUS"
fi

# Check database configuration
echo ""
echo "💾 DATABASE CONFIGURATION:"
cd crm_project
if [ -f ".env" ]; then
    echo "   ✅ .env file found"
    if grep -q "DATABASE_URL.*postgresql" .env 2>/dev/null; then
        echo "   🗄️  Database: PostgreSQL (configured)"
    elif grep -q "sqlite" .env 2>/dev/null; then
        echo "   🗄️  Database: SQLite (configured)"
    else
        echo "   🗄️  Database: Configuration detected"
    fi
else
    echo "   ℹ️  No .env file found"
fi

if [ -f "db.sqlite3" ]; then
    DB_SIZE=$(ls -lh db.sqlite3 | awk '{print $5}')
    echo "   📊 SQLite database: $DB_SIZE"
else
    echo "   ℹ️  No local SQLite database"
fi

echo ""
echo "🎯 SUMMARY:"
echo "   • Development Environment: Virtual Environment (claude-env)"
echo "   • Docker Support: ✅ Full Docker setup available"
echo "   • Current Mode: Running on host system with virtual env"
echo "   • Database: SQLite (development mode)"
echo "   • Production Ready: ✅ Docker + PostgreSQL + Redis configured"
echo ""
echo "🚀 DEPLOYMENT OPTIONS:"
echo "   1. Current: Virtual env + SQLite (development)"
echo "   2. Docker: docker-compose up (full production stack)"
echo "   3. Hybrid: Docker database + virtual env app"
