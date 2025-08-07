#!/bin/bash
# Start CRM server for multi-device testing on MacBook
# This script allows other devices on your network to access the CRM application

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}🚀 Starting CRM Testing Server for Multi-Device Access${NC}"

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$SCRIPT_DIR/crm_project"

# Check if project directory exists
if [ ! -d "$PROJECT_DIR" ]; then
    echo -e "${RED}❌ Project directory not found: $PROJECT_DIR${NC}"
    exit 1
fi

# Navigate to project directory
cd "$PROJECT_DIR"

# Check if virtual environment exists
if [ ! -d "../venv" ]; then
    echo -e "${RED}❌ Virtual environment not found. Please set up your project first.${NC}"
    exit 1
fi

# Activate virtual environment
source ../venv/bin/activate

# Use testing environment
export DJANGO_SETTINGS_MODULE=crm_project.settings
echo -e "${YELLOW}📝 Using testing environment configuration${NC}"

# Copy testing environment file
if [ -f ".env.testing" ]; then
    cp .env.testing .env
    echo -e "${GREEN}✅ Testing environment configured${NC}"
else
    echo -e "${YELLOW}⚠️  .env.testing not found, using current .env${NC}"
fi

# Get local IP addresses
echo -e "${BLUE}🌐 Network Information:${NC}"
LOCAL_IPS=$(ifconfig | grep "inet " | grep -v "127.0.0.1" | awk '{print $2}')
echo -e "${GREEN}   Local IP addresses:${NC}"
echo "$LOCAL_IPS" | while read ip; do
    if [ ! -z "$ip" ]; then
        echo -e "${GREEN}   • http://$ip:8000${NC}"
    fi
done

echo ""
echo -e "${BLUE}📱 Access URLs for testing devices:${NC}"
echo -e "${GREEN}   • Local: http://localhost:8000${NC}"
echo -e "${GREEN}   • Local: http://127.0.0.1:8000${NC}"
echo "$LOCAL_IPS" | while read ip; do
    if [ ! -z "$ip" ]; then
        echo -e "${GREEN}   • Network: http://$ip:8000${NC}"
    fi
done

echo ""
echo -e "${BLUE}🔧 API Endpoints:${NC}"
echo -e "${GREEN}   • API Root: /api/v1/${NC}"
echo -e "${GREEN}   • Admin Panel: /admin/${NC}"
echo -e "${GREEN}   • UAT Dashboard: /dashboard/${NC}"

echo ""
echo -e "${YELLOW}⚠️  Testing Mode Active:${NC}"
echo -e "${YELLOW}   • DEBUG = True${NC}"
echo -e "${YELLOW}   • CORS allows all origins${NC}"
echo -e "${YELLOW}   • Relaxed security settings${NC}"
echo -e "${YELLOW}   • Use UAT access token: test-access-token-123${NC}"

echo ""
echo -e "${BLUE}🚀 Starting Django development server...${NC}"
echo -e "${YELLOW}💡 Press Ctrl+C to stop the server${NC}"
echo ""

# Start the development server with network access
python manage.py runserver 0.0.0.0:8000