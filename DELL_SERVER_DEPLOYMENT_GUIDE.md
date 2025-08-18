# Dell Server Deployment Guide - Company CRM System

## Overview

This guide provides complete instructions for deploying the Company CRM System on a Dell server for production use with both intranet and internet access. The CRM system is built with Django and includes customer management, communication tools, and comprehensive reporting features.

## Prerequisites

- Dell server with Ubuntu 24.04 LTS (recommended) or Ubuntu 22.04 LTS
- Root access to the server
- Network connectivity (intranet and internet)
- At least 8GB RAM and 50GB storage
- Python 3.8+ and Git installed on the server

## Quick Start

For immediate deployment, follow these steps:

```bash
# 1. Clone or copy the application to the server
git clone <repository-url> /tmp/company_crm_system
cd /tmp/company_crm_system

# 2. Install production dependencies
sudo ./scripts/install-production-deps.sh

# 3. Deploy the application
sudo ./scripts/deploy.sh

# 4. Configure environment (edit as needed)
sudo nano /opt/company_crm_system/.env

# 5. Restart services
sudo systemctl restart company-crm
sudo systemctl restart nginx
```

The application will be available at `http://server-ip:8082`

## Detailed Deployment Steps

### Step 1: System Preparation

1. **Update the system:**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. **Install required system packages:**
   ```bash
   sudo apt install -y python3 python3-venv python3-pip python3-dev
   sudo apt install -y postgresql postgresql-contrib
   sudo apt install -y redis-server
   sudo apt install -y nginx git curl
   ```

3. **Clone the repository:**
   ```bash
   git clone <repository-url> /tmp/company_crm_system
   cd /tmp/company_crm_system
   ```

### Step 2: Database Setup

#### PostgreSQL Configuration

```bash
# Switch to postgres user
sudo -u postgres psql

# Create database and user
CREATE DATABASE company_crm_db;
CREATE USER crm_user WITH PASSWORD 'secure_password_here';
GRANT ALL PRIVILEGES ON DATABASE company_crm_db TO crm_user;
ALTER USER crm_user CREATEDB;
\q
```

#### Redis Configuration

```bash
# Start and enable Redis
sudo systemctl start redis-server
sudo systemctl enable redis-server

# Test Redis connection
redis-cli ping
```

### Step 3: Application Setup

1. **Create application directory:**
   ```bash
   sudo mkdir -p /opt/company_crm_system
   sudo cp -r . /opt/company_crm_system/
   cd /opt/company_crm_system
   ```

2. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   ```bash
   sudo cp .env.production.example .env
   sudo nano .env
   ```

### Step 4: Environment Configuration

Edit the environment configuration file:

```bash
sudo nano /opt/company_crm_system/.env
```

Key settings to configure:

```bash
# Security
SECRET_KEY=your_generated_secret_key_here
DEBUG=False

# Database Configuration (Production PostgreSQL)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=company_crm_db
DB_USER=crm_user
DB_PASSWORD=secure_password_here
DB_HOST=localhost
DB_PORT=5432

# Server Configuration
PORT=8082
ALLOWED_HOSTS=your-server-ip,your-domain.com,localhost,127.0.0.1

# Redis Configuration
REDIS_URL=redis://localhost:6379/0

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@company.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@company.com

# Communication APIs (Optional)
WHATSAPP_ACCESS_TOKEN=your-whatsapp-token
WHATSAPP_PHONE_NUMBER_ID=your-phone-number-id
WECHAT_CORP_ID=your-corp-id
WECHAT_CORP_SECRET=your-corp-secret
WECHAT_AGENT_ID=your-agent-id
```

### Step 5: Django Application Setup

```bash
cd /opt/company_crm_system/crm_project

# Activate virtual environment
source ../venv/bin/activate

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

### Step 6: Systemd Service Configuration

Create systemd service file:

```bash
sudo nano /etc/systemd/system/company-crm.service
```

Service file content:

```ini
[Unit]
Description=Company CRM Django Application
After=network.target postgresql.service redis.service
Requires=postgresql.service redis.service

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/opt/company_crm_system/crm_project
Environment=DJANGO_SETTINGS_MODULE=crm_project.settings
ExecStart=/opt/company_crm_system/venv/bin/python manage.py runserver 0.0.0.0:8082
ExecReload=/bin/kill -HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true
WatchdogSec=120

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable company-crm
sudo systemctl start company-crm
```

### Step 7: Nginx Reverse Proxy Setup

Create Nginx configuration:

```bash
sudo nano /etc/nginx/sites-available/company-crm
```

Nginx configuration:

```nginx
server {
    listen 80;
    server_name your-domain.com your-server-ip;
    
    client_max_body_size 10M;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    
    # Rate limiting
    limit_req_zone $binary_remote_addr zone=crm:10m rate=10r/m;
    
    location / {
        limit_req zone=crm burst=20 nodelay;
        proxy_pass http://127.0.0.1:8082;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    location /static/ {
        alias /opt/company_crm_system/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    location /media/ {
        alias /opt/company_crm_system/media/;
        expires 1y;
        add_header Cache-Control "public";
    }
}
```

Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/company-crm /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Network Configuration

### Firewall Settings

Configure UFW firewall:

```bash
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw allow 8082/tcp
sudo ufw enable
```

### Port Configuration

- **Port 22** (SSH) - Open for administration
- **Port 80** (HTTP) - Open for web access
- **Port 443** (HTTPS) - Open for secure web access
- **Port 8082** - CRM application port (proxied through Nginx)

## Security Configuration

### File Permissions

Set proper file ownership and permissions:

```bash
sudo chown -R www-data:www-data /opt/company_crm_system
sudo chmod -R 755 /opt/company_crm_system
sudo chmod -R 644 /opt/company_crm_system/.env
```

### Database Security

```bash
# PostgreSQL security
sudo nano /etc/postgresql/*/main/postgresql.conf
# Set: listen_addresses = 'localhost'

sudo nano /etc/postgresql/*/main/pg_hba.conf
# Ensure local connections use md5 authentication
```

### Redis Security

```bash
sudo nano /etc/redis/redis.conf
# Set: bind 127.0.0.1
# Set: requirepass your_redis_password
sudo systemctl restart redis-server
```

## Dell Hardware-Specific Optimizations

### Network Adapter Optimization

```bash
# Check Dell network adapter
sudo lspci | grep -E "(Network|Ethernet)"
sudo ethtool eth0

# Optimize for Dell hardware
sudo ethtool -G eth0 rx 2048 tx 2048
sudo ethtool -K eth0 tso on gso on
```

### Memory Optimization for Dell Servers

```bash
# Check memory configuration
free -h
sudo nano /etc/sysctl.conf

# Add Dell-optimized settings
vm.swappiness=10
vm.vfs_cache_pressure=50
vm.dirty_ratio=15
vm.dirty_background_ratio=5

sudo sysctl -p
```

### Dell BIOS/UEFI Recommendations

- **Power Management**: Set to "OS Control"
- **Virtualization Technology**: Enable if using containers
- **Network Stack**: Enable for PXE boot if needed
- **Secure Boot**: Enable for additional security
- **SATA Operation**: Set to AHCI mode

## Performance Tuning

### Django Production Settings

Update settings for production:

```python
# In crm_project/settings.py
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com', 'server-ip']

# Database connection pooling
DATABASES['default']['CONN_MAX_AGE'] = 600

# Caching
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

### Gunicorn Configuration (Optional)

For better production performance, use Gunicorn:

```bash
pip install gunicorn
```

Create Gunicorn service:

```bash
sudo nano /etc/systemd/system/company-crm-gunicorn.service
```

```ini
[Unit]
Description=Company CRM Gunicorn Application Server
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/opt/company_crm_system/crm_project
ExecStart=/opt/company_crm_system/venv/bin/gunicorn \
    --workers 3 \
    --timeout 120 \
    --max-requests 1000 \
    --bind 0.0.0.0:8082 \
    crm_project.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

## Monitoring and Maintenance

### System Health Checks

Create health check script:

```bash
sudo nano /usr/local/bin/crm-health-check
```

```bash
#!/bin/bash
echo "=== CRM System Health Check ==="
echo "Date: $(date)"
echo ""

echo "Service Status:"
systemctl is-active company-crm
systemctl is-active postgresql
systemctl is-active redis-server
systemctl is-active nginx

echo ""
echo "Port Status:"
netstat -tulpn | grep :8082
netstat -tulpn | grep :80

echo ""
echo "Database Connection:"
sudo -u postgres psql -d company_crm_db -c "SELECT 1;" > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "PostgreSQL: OK"
else
    echo "PostgreSQL: FAILED"
fi

echo ""
echo "Redis Connection:"
redis-cli ping > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "Redis: OK"
else
    echo "Redis: FAILED"
fi

echo ""
echo "Application Response:"
curl -s -o /dev/null -w "%{http_code}" http://localhost:8082/ | grep -q "200\|302"
if [ $? -eq 0 ]; then
    echo "CRM Application: OK"
else
    echo "CRM Application: FAILED"
fi
```

Make it executable:

```bash
sudo chmod +x /usr/local/bin/crm-health-check
```

### Log Management

Configure log rotation:

```bash
sudo nano /etc/logrotate.d/company-crm
```

```
/opt/company_crm_system/logs/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 0644 www-data www-data
    postrotate
        systemctl reload company-crm
    endscript
}
```

### Backup Strategy

Create backup script:

```bash
sudo nano /usr/local/bin/backup-company-crm
```

```bash
#!/bin/bash
BACKUP_DIR="/var/backups/company-crm"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p "$BACKUP_DIR/$DATE"

# Database backup
sudo -u postgres pg_dump company_crm_db > "$BACKUP_DIR/$DATE/database.sql"

# Application files backup
tar -czf "$BACKUP_DIR/$DATE/application.tar.gz" /opt/company_crm_system

# Media files backup
tar -czf "$BACKUP_DIR/$DATE/media.tar.gz" /opt/company_crm_system/media

# Keep only last 30 days of backups
find "$BACKUP_DIR" -type d -mtime +30 -exec rm -rf {} +

echo "Backup completed: $BACKUP_DIR/$DATE"
```

Make executable and schedule:

```bash
sudo chmod +x /usr/local/bin/backup-company-crm

# Add to crontab for daily backups at 2 AM
sudo crontab -e
# Add: 0 2 * * * /usr/local/bin/backup-company-crm
```

## Troubleshooting

### Common Issues

1. **Service won't start:**
   ```bash
   sudo journalctl -u company-crm -n 50
   sudo systemctl status company-crm
   ```

2. **Database connection errors:**
   ```bash
   # Check PostgreSQL status
   sudo systemctl status postgresql
   
   # Test connection
   sudo -u postgres psql -d company_crm_db -c "SELECT version();"
   ```

3. **Redis connection issues:**
   ```bash
   # Check Redis status
   sudo systemctl status redis-server
   
   # Test connection
   redis-cli ping
   ```

4. **Port accessibility issues:**
   ```bash
   # Check if application is listening
   sudo netstat -tulpn | grep :8082
   
   # Check firewall
   sudo ufw status
   ```

5. **Permission errors:**
   ```bash
   # Fix ownership
   sudo chown -R www-data:www-data /opt/company_crm_system
   
   # Check logs
   sudo tail -f /var/log/nginx/error.log
   ```

### Performance Issues

Monitor resource usage:

```bash
# Check CPU and memory
htop

# Check disk usage
df -h

# Check database performance
sudo -u postgres psql -d company_crm_db -c "SELECT * FROM pg_stat_activity;"
```

## SSL/HTTPS Configuration (Optional)

To enable HTTPS:

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain SSL certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo systemctl enable certbot.timer
```

## Maintenance Schedule

### Regular Tasks

- **Daily**: Check system health and review logs
- **Weekly**: Review performance metrics and disk usage
- **Monthly**: Update system packages and review security
- **Quarterly**: Review and update backup procedures

### Monitoring Checklist

- [ ] CRM application responding (http://server-ip:8082)
- [ ] All services running (systemctl status)
- [ ] Database connectivity working
- [ ] Redis cache operational
- [ ] Disk space sufficient (df -h)
- [ ] Memory usage reasonable (free -h)
- [ ] Recent backups completed
- [ ] Security updates applied

## Quick Reference

### Essential Commands

```bash
# Service management
sudo systemctl status company-crm
sudo systemctl restart company-crm

# View application logs
sudo journalctl -u company-crm -f

# Django management
cd /opt/company_crm_system/crm_project
source ../venv/bin/activate
python manage.py shell

# Health check
sudo /usr/local/bin/crm-health-check

# Backup
sudo /usr/local/bin/backup-company-crm
```

### File Locations

- **Application**: `/opt/company_crm_system/`
- **Virtual Environment**: `/opt/company_crm_system/venv/`
- **Django Project**: `/opt/company_crm_system/crm_project/`
- **Configuration**: `/opt/company_crm_system/.env`
- **Static Files**: `/opt/company_crm_system/staticfiles/`
- **Media Files**: `/opt/company_crm_system/media/`
- **Backups**: `/var/backups/company-crm/`
- **Logs**: `/opt/company_crm_system/logs/`

### Access URLs

- **Application**: `http://server-ip:8082`
- **Admin Panel**: `http://server-ip:8082/admin/`
- **API Root**: `http://server-ip:8082/api/v1/`
- **UAT Dashboard**: `http://server-ip:8082/dashboard/`

This deployment guide ensures a secure, scalable, and maintainable installation of the Company CRM System on your Dell server with optimal performance and reliability.