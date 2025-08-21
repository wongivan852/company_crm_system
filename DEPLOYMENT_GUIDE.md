# CRM System Production Deployment Guide

## Overview
This guide covers the production deployment of the enhanced CRM system with all security, performance, and monitoring improvements implemented.

## 🔐 Security Features Implemented

### 1. SSL/HTTPS Configuration
- ✅ Nginx reverse proxy with SSL termination
- ✅ Automatic HTTP to HTTPS redirect  
- ✅ HSTS headers with 1-year max-age
- ✅ Security headers (X-Frame-Options, X-Content-Type-Options, etc.)

### 2. Security Middleware
- ✅ Rate limiting (API: 1000/hour, Login: 5/5min)
- ✅ Security audit logging
- ✅ Suspicious pattern detection
- ✅ IP-based access controls

### 3. Production Security Settings
- ✅ Fixed ALLOWED_HOSTS (no wildcards)
- ✅ Secure cookie settings
- ✅ CSRF protection
- ✅ Content Security Policy

## 📊 Monitoring & Health Checks

### Available Endpoints
- `GET /health/` - System health status
- `GET /metrics/` - Detailed metrics (authenticated)
- `GET /api/v1/customers/data_quality/` - Data quality report

### Health Check Response
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00Z",
  "checks": {
    "database": {"status": "healthy"},
    "redis": {"status": "healthy"},
    "application": {"status": "healthy"}
  },
  "metrics": {
    "total_customers": 1010,
    "active_customers": 932
  }
}
```

## 🗄️ Database Performance

### Implemented Indexes
- **Full-text search**: Customer names, emails, companies
- **Email search**: Case-insensitive email lookups  
- **Phone search**: Cleaned phone number matching
- **Partial indexes**: Active customers, recent data
- **Covering indexes**: Frequent query optimization

### Performance Features
- ✅ Connection pooling (600s max age)
- ✅ Query optimization with select_related/prefetch_related
- ✅ Redis caching (3-layer strategy)
- ✅ Automated backup system

## 🚀 Deployment Steps

### 1. Prerequisites
```bash
# Install Docker and Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install docker-compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 2. Environment Setup
```bash
# Copy production environment template
cp .env.prod.example .env.prod

# Edit environment variables
nano .env.prod
```

Required environment variables:
```bash
# Security
SECRET_KEY=your-super-secret-key-minimum-50-characters-long
DOMAIN_NAME=your-domain.com

# Database
DB_PASSWORD=secure-database-password-here

# Email (optional)
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### 3. SSL Certificate Setup
```bash
# Create SSL directory
mkdir -p nginx/ssl

# Option A: Let's Encrypt (recommended)
sudo apt install certbot python3-certbot-nginx
certbot certonly --standalone -d your-domain.com

# Copy certificates
sudo cp /etc/letsencrypt/live/your-domain.com/fullchain.pem nginx/ssl/cert.pem
sudo cp /etc/letsencrypt/live/your-domain.com/privkey.pem nginx/ssl/key.pem

# Option B: Self-signed (development only)
openssl req -x509 -newkey rsa:4096 -keyout nginx/ssl/key.pem -out nginx/ssl/cert.pem -days 365 -nodes
```

### 4. Production Deployment
```bash
# Deploy with production configuration
docker-compose -f docker-compose.prod.yml up -d

# Run database migrations
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate

# Create superuser
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser

# Collect static files
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput

# Run data quality fixes (if needed)
docker-compose -f docker-compose.prod.yml exec web python manage.py fix_data_quality
```

### 5. Backup Setup
```bash
# Make backup script executable
chmod +x scripts/backup_database.sh

# Add to crontab
crontab -e

# Add this line for daily backups at 2 AM
0 2 * * * cd /path/to/company_crm_system && ./scripts/backup_database.sh
```

## 📊 Data Quality Improvements

### Implemented Fixes
- ✅ Email validation and cleaning
- ✅ Country detection from email domains
- ✅ Phone number normalization
- ✅ Name formatting standardization

### Data Quality Commands
```bash
# Generate data quality report
python manage.py fix_data_quality --report-only

# Fix data quality issues
python manage.py fix_data_quality

# API endpoint for data quality
curl -X GET http://localhost:8083/api/v1/customers/data_quality/
```

## 🎯 API Endpoints

### Authentication Required Endpoints
```bash
# Customer operations
GET    /api/v1/customers/              # List customers
POST   /api/v1/customers/              # Create customer
GET    /api/v1/customers/{id}/         # Get customer
PUT    /api/v1/customers/{id}/         # Update customer
DELETE /api/v1/customers/{id}/         # Delete customer

# Data operations
POST   /api/v1/customers/import_csv/   # Import CSV
GET    /api/v1/customers/export_csv/   # Export CSV
GET    /api/v1/customers/data_quality/ # Data quality report
POST   /api/v1/customers/data_quality/ # Fix data quality

# Communication
POST   /api/v1/customers/{id}/send_message/ # Send message

# Search
GET    /api/v1/customers/search_by_contact/?contact=email@domain.com
```

### Public Endpoints
```bash
GET    /health/                        # Health check
GET    /metrics/                      # Metrics (authenticated)
```

## 🔧 Maintenance

### Regular Tasks
```bash
# Weekly database maintenance
docker-compose exec db psql -U crm_user -d crm_db -c "VACUUM ANALYZE;"

# Monthly performance analysis
docker-compose exec web python manage.py analyze_db_performance

# Check system health
curl -f http://localhost/health/ || echo "System unhealthy"

# Monitor logs
docker-compose logs -f --tail=50 web
```

### Backup and Restore
```bash
# Manual backup
./scripts/backup_database.sh

# Restore from backup
./scripts/restore_database.sh crm_backup_20241221_143022.sql.gz

# Verify backup
gunzip -t backups/crm_backup_20241221_143022.sql.gz
```

## 🚨 Monitoring and Alerts

### Health Monitoring
```bash
# Set up monitoring script
#!/bin/bash
HEALTH_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost/health/)
if [ $HEALTH_STATUS -ne 200 ]; then
    echo "CRM System is unhealthy (HTTP $HEALTH_STATUS)" | mail -s "CRM Alert" admin@yourcompany.com
fi
```

### Log Monitoring
```bash
# Monitor error logs
tail -f logs/crm_errors.log

# Monitor security logs  
tail -f logs/security.log

# Monitor performance
tail -f logs/performance.log
```

## 🔄 Updates and Rollback

### Update Deployment
```bash
# Pull latest changes
git pull origin main

# Backup database before update
./scripts/backup_database.sh

# Update with zero downtime
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d

# Run any new migrations
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
```

### Rollback Process
```bash
# Stop current services
docker-compose -f docker-compose.prod.yml down

# Checkout previous version
git checkout HEAD~1

# Restore database if needed
./scripts/restore_database.sh latest_backup.sql.gz

# Start services
docker-compose -f docker-compose.prod.yml up -d
```

## 📈 Performance Metrics

### Expected Performance
- **API Response Time**: < 200ms (95th percentile)
- **Database Query Time**: < 100ms (average)
- **Page Load Time**: < 2 seconds
- **Import Performance**: 1000 records/minute
- **Cache Hit Rate**: > 80%

### Performance Monitoring
```bash
# Database performance analysis
docker-compose exec web python manage.py analyze_db_performance --all

# Check cache performance
redis-cli info stats | grep keyspace_hits

# Monitor API response times
grep "X-Response-Time" nginx/access.log | awk '{print $NF}' | sort -n
```

## 🛠️ Troubleshooting

### Common Issues

**1. SSL Certificate Issues**
```bash
# Check certificate validity
openssl x509 -in nginx/ssl/cert.pem -text -noout

# Renew Let's Encrypt certificate
certbot renew --dry-run
```

**2. Database Connection Issues**
```bash
# Check database logs
docker-compose logs db

# Test database connection
docker-compose exec web python manage.py dbshell
```

**3. Performance Issues**
```bash
# Check slow queries
docker-compose exec web python manage.py analyze_db_performance --slow-queries

# Monitor system resources
docker stats
```

**4. Data Quality Issues**
```bash
# Run data quality analysis
docker-compose exec web python manage.py fix_data_quality --report-only

# Fix specific issues
curl -X POST http://localhost/api/v1/customers/data_quality/ -d '{"action":"fix_all"}'
```

## 🔐 Security Checklist

- [ ] SSL certificates installed and valid
- [ ] ALLOWED_HOSTS configured (no wildcards)
- [ ] Strong SECRET_KEY (50+ characters)
- [ ] Database password changed from default
- [ ] Rate limiting enabled
- [ ] Security headers configured
- [ ] Backup encryption enabled
- [ ] Log monitoring configured
- [ ] Regular security updates scheduled

## 📞 Support

### System Status
- Health Check: `curl https://your-domain.com/health/`
- Metrics: `curl -u username:password https://your-domain.com/metrics/`

### Contact Information
- System Administrator: [your-email@domain.com]
- Emergency Contact: [emergency-contact@domain.com]
- Documentation: [internal-docs-url]

---

**Last Updated**: December 21, 2024  
**Version**: 1.0.0  
**Status**: Production Ready ✅