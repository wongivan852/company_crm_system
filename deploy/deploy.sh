#!/bin/bash
# CRM Application Deployment Script for Ubuntu Server
# Run this script as the crmuser on Ubuntu server

set -e  # Exit on any error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Starting CRM Application Deployment...${NC}"

# Check if running as correct user
if [ "$USER" != "crmuser" ]; then
    echo -e "${RED}❌ This script should be run as 'crmuser'${NC}"
    echo -e "${YELLOW}💡 Switch user: sudo su - crmuser${NC}"
    exit 1
fi

# Set deployment directory
DEPLOY_DIR="/opt/crm"
PROJECT_DIR="$DEPLOY_DIR/crm_project"

# Navigate to deployment directory
cd $DEPLOY_DIR

echo -e "${BLUE}📂 Setting up project structure...${NC}"

# Check if git repository exists
if [ ! -d ".git" ]; then
    echo -e "${YELLOW}⚠️  Git repository not found in $DEPLOY_DIR${NC}"
    echo -e "${YELLOW}💡 Please clone your CRM repository here first${NC}"
    echo -e "${YELLOW}   Example: git clone your-repo-url .${NC}"
    exit 1
fi

# Pull latest code
echo -e "${BLUE}📥 Pulling latest code...${NC}"
git pull origin main

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "${BLUE}🐍 Creating Python virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo -e "${BLUE}📦 Upgrading pip...${NC}"
pip install --upgrade pip

# Install requirements
echo -e "${BLUE}📋 Installing Python dependencies...${NC}"
pip install -r crm_project/requirements.ubuntu.txt

# Copy production environment file if it exists
if [ -f "crm_project/.env.production" ]; then
    echo -e "${BLUE}⚙️  Setting up production environment...${NC}"
    cp crm_project/.env.production crm_project/.env
else
    echo -e "${YELLOW}⚠️  .env.production file not found${NC}"
    echo -e "${YELLOW}💡 Please create .env file with production settings${NC}"
fi

# Navigate to project directory
cd $PROJECT_DIR

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo -e "${RED}❌ .env file not found${NC}"
    echo -e "${YELLOW}💡 Please create .env file with production configuration${NC}"
    exit 1
fi

# Run database migrations
echo -e "${BLUE}🗃️  Running database migrations...${NC}"
python manage.py migrate --noinput

# Collect static files
echo -e "${BLUE}🎨 Collecting static files...${NC}"
python manage.py collectstatic --noinput --clear

# Create superuser (interactive)
echo -e "${BLUE}👤 Creating Django superuser...${NC}"
echo -e "${YELLOW}💡 You'll be prompted to create an admin user${NC}"
python manage.py createsuperuser || echo "Superuser creation skipped"

# Warm cache for better performance
echo -e "${BLUE}🔥 Warming application cache...${NC}"
python manage.py warm_cache --clear-first --verbose

# Set proper permissions
echo -e "${BLUE}🔒 Setting file permissions...${NC}"
find $DEPLOY_DIR -type f -exec chmod 644 {} \;
find $DEPLOY_DIR -type d -exec chmod 755 {} \;
chmod +x $DEPLOY_DIR/deploy/*.sh

# Create necessary directories
mkdir -p $DEPLOY_DIR/static
mkdir -p $DEPLOY_DIR/media
mkdir -p /var/log/crm
mkdir -p /var/run/crm

# Set ownership
sudo chown -R crmuser:crmuser $DEPLOY_DIR
sudo chown -R crmuser:crmuser /var/log/crm
sudo chown -R crmuser:crmuser /var/run/crm

# Test Django application
echo -e "${BLUE}🧪 Testing Django application...${NC}"
python manage.py check --deploy

# Restart services
echo -e "${BLUE}🔄 Restarting services...${NC}"

# Reload systemd and restart supervisor programs
sudo systemctl daemon-reload
sudo supervisorctl reread
sudo supervisorctl update

# Start/restart CRM services
sudo supervisorctl restart crm
sudo supervisorctl restart crm-celery

# Restart Nginx
sudo systemctl restart nginx

# Check service status
echo -e "${BLUE}📊 Checking service status...${NC}"
echo -e "${YELLOW}Supervisor status:${NC}"
sudo supervisorctl status

echo -e "${YELLOW}Nginx status:${NC}"
sudo systemctl status nginx --no-pager -l

echo -e "${YELLOW}PostgreSQL status:${NC}"
sudo systemctl status postgresql --no-pager -l

echo -e "${YELLOW}Redis status:${NC}"
sudo systemctl status redis-server --no-pager -l

# Show application URLs
echo -e "${GREEN}✅ Deployment completed successfully!${NC}"
echo -e "${GREEN}🌐 Your CRM application should now be available at:${NC}"
echo -e "${BLUE}   HTTP: http://your-domain.com${NC}"
echo -e "${BLUE}   Admin: http://your-domain.com/admin/${NC}"
echo -e "${BLUE}   API: http://your-domain.com/api/v1/${NC}"

echo ""
echo -e "${YELLOW}📋 Post-deployment checklist:${NC}"
echo -e "${YELLOW}   □ Update domain name in /etc/nginx/sites-available/crm${NC}"
echo -e "${YELLOW}   □ Set up SSL certificate: sudo certbot --nginx -d your-domain.com${NC}"
echo -e "${YELLOW}   □ Test all application features${NC}"
echo -e "${YELLOW}   □ Set up backup strategy${NC}"
echo -e "${YELLOW}   □ Configure monitoring (optional)${NC}"

echo ""
echo -e "${YELLOW}🔧 Useful commands:${NC}"
echo -e "${YELLOW}   View logs: sudo tail -f /var/log/crm/gunicorn.log${NC}"
echo -e "${YELLOW}   Restart app: sudo supervisorctl restart crm${NC}"
echo -e "${YELLOW}   Check status: sudo supervisorctl status${NC}"
echo -e "${YELLOW}   Update code: cd /opt/crm && git pull && sudo supervisorctl restart crm${NC}"

echo ""
echo -e "${GREEN}🎉 Deployment complete! Happy coding!${NC}"