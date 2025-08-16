#!/bin/bash
# Ubuntu Server Setup Script for CRM Deployment
# Run as root or with sudo privileges

set -e  # Exit on any error

echo "🚀 Starting CRM Ubuntu Server Setup..."

# Update system
echo "📦 Updating system packages..."
apt-get update && apt-get upgrade -y

# Install system dependencies
echo "🔧 Installing system dependencies..."
apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    postgresql \
    postgresql-contrib \
    redis-server \
    nginx \
    git \
    curl \
    wget \
    supervisor \
    certbot \
    python3-certbot-nginx \
    ufw \
    htop \
    nano \
    vim

# Configure firewall
echo "🔒 Configuring firewall..."
ufw --force enable
ufw allow ssh
ufw allow 80
ufw allow 443
ufw allow 8000  # For development/testing

# Create CRM user
echo "👤 Creating CRM application user..."
if ! id "crmuser" &>/dev/null; then
    useradd -m -s /bin/bash crmuser
    usermod -aG sudo crmuser
    echo "Created user: crmuser"
else
    echo "User crmuser already exists"
fi

# Create application directory
echo "📁 Creating application directories..."
mkdir -p /opt/crm
chown crmuser:crmuser /opt/crm

mkdir -p /var/log/crm
chown crmuser:crmuser /var/log/crm

mkdir -p /var/run/crm
chown crmuser:crmuser /var/run/crm

# Setup PostgreSQL
echo "🐘 Setting up PostgreSQL..."
systemctl enable postgresql
systemctl start postgresql

# Create database and user (run as postgres user)
sudo -u postgres psql << EOF
CREATE DATABASE crm_production;
CREATE USER crm_user WITH PASSWORD 'change_this_password_in_production';
GRANT ALL PRIVILEGES ON DATABASE crm_production TO crm_user;
ALTER USER crm_user CREATEDB;
\q
EOF

# Configure Redis
echo "📮 Configuring Redis..."
systemctl enable redis-server
systemctl start redis-server

# Configure Redis for production
cat > /etc/redis/redis.conf.backup << EOF
# Backup created by CRM setup script
EOF
cp /etc/redis/redis.conf /etc/redis/redis.conf.backup

# Basic Redis security
sed -i 's/# requirepass foobared/requireauth your_redis_password_here/' /etc/redis/redis.conf
sed -i 's/bind 127.0.0.1 ::1/bind 127.0.0.1/' /etc/redis/redis.conf
systemctl restart redis-server

# Setup Nginx
echo "🌐 Setting up Nginx..."
systemctl enable nginx

# Create Nginx configuration for CRM
cat > /etc/nginx/sites-available/crm << 'EOF'
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;  # Change this

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /opt/crm;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    location /media/ {
        root /opt/crm;
        expires 1y;
        add_header Cache-Control "public";
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/run/crm/crm.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeout settings
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
EOF

# Enable the site
ln -sf /etc/nginx/sites-available/crm /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Test Nginx configuration
nginx -t

# Setup Supervisor for Gunicorn
echo "👨‍💼 Setting up Supervisor..."
cat > /etc/supervisor/conf.d/crm.conf << 'EOF'
[program:crm]
command=/opt/crm/venv/bin/gunicorn --workers 3 --bind unix:/var/run/crm/crm.sock crm_project.wsgi:application
directory=/opt/crm/crm_project
user=crmuser
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/crm/gunicorn.log
environment=PATH="/opt/crm/venv/bin"

[program:crm-celery]
command=/opt/crm/venv/bin/celery -A crm_project worker --loglevel=info
directory=/opt/crm/crm_project
user=crmuser
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/crm/celery.log
environment=PATH="/opt/crm/venv/bin"
EOF

# Create systemctl service files as backup
cat > /etc/systemd/system/crm.service << 'EOF'
[Unit]
Description=CRM Django Application
After=network.target

[Service]
Type=notify
User=crmuser
Group=crmuser
WorkingDirectory=/opt/crm/crm_project
Environment=PATH=/opt/crm/venv/bin
ExecStart=/opt/crm/venv/bin/gunicorn --workers 3 --bind unix:/var/run/crm/crm.sock crm_project.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

# Set up log rotation
cat > /etc/logrotate.d/crm << 'EOF'
/var/log/crm/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 crmuser crmuser
    postrotate
        supervisorctl restart crm
        supervisorctl restart crm-celery
    endscript
}
EOF

echo "✅ Ubuntu server setup completed!"
echo ""
echo "📋 Next steps:"
echo "1. Switch to crmuser: sudo su - crmuser"
echo "2. Clone your CRM repository to /opt/crm/"
echo "3. Run the deployment script: ./deploy.sh"
echo "4. Update domain name in /etc/nginx/sites-available/crm"
echo "5. Set up SSL with: sudo certbot --nginx -d your-domain.com"
echo ""
echo "🔐 Security reminders:"
echo "- Change PostgreSQL password in .env.production"
echo "- Update Redis password in /etc/redis/redis.conf"
echo "- Configure proper backup strategy"
echo "- Set up monitoring (optional)"
echo ""
echo "🎯 System is ready for CRM deployment!"