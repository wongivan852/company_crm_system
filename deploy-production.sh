#!/bin/bash

# Production Deployment Script for CRM System
# Supports both Internet and Intranet Access

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING:${NC} $1"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR:${NC} $1"
    exit 1
}

# Check if running as root
check_root() {
    if [[ $EUID -eq 0 ]]; then
        error "Do not run this script as root. Run as the application user."
    fi
}

# Check prerequisites
check_prerequisites() {
    log "Checking prerequisites..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        error "Docker is not installed. Please install Docker first."
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        error "Docker Compose is not installed. Please install Docker Compose first."
    fi
    
    # Check if user is in docker group
    if ! groups $USER | grep -q docker; then
        warn "User $USER is not in the docker group. You may need to run docker commands with sudo."
    fi
}

# Setup environment files
setup_environment() {
    log "Setting up environment configuration..."
    
    if [[ ! -f .env.production ]]; then
        log "Creating .env.production file..."
        cat > .env.production << 'EOF'
# Production Environment Configuration
DEBUG=0
SECRET_KEY=your-super-secret-key-change-this-in-production
ALLOWED_HOSTS=your-domain.com,www.your-domain.com,localhost,127.0.0.1

# Database Configuration
DB_PASSWORD=your-secure-db-password

# Redis Configuration  
REDIS_PASSWORD=your-secure-redis-password

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Security Settings
SECURE_SSL_REDIRECT=1
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=1
SECURE_HSTS_PRELOAD=1
SESSION_COOKIE_SECURE=1
CSRF_COOKIE_SECURE=1
EOF
        warn "Please edit .env.production and update all configuration values!"
        warn "Default passwords and secrets are NOT secure!"
        read -p "Press Enter after updating .env.production to continue..."
    fi
    
    # Copy environment file
    cp .env.production .env
}

# Setup SSL certificates
setup_ssl() {
    log "Setting up SSL certificates..."
    
    if [[ ! -d ssl ]]; then
        mkdir -p ssl
        log "Created ssl directory for certificates"
    fi
    
    if [[ ! -f ssl/your-domain.crt ]] || [[ ! -f ssl/your-domain.key ]]; then
        warn "SSL certificates not found in ssl/ directory"
        echo "Options:"
        echo "1. Place your SSL certificates in ssl/your-domain.crt and ssl/your-domain.key"
        echo "2. Generate self-signed certificates for testing"
        read -p "Generate self-signed certificates for testing? (y/N): " generate_ssl
        
        if [[ $generate_ssl =~ ^[Yy]$ ]]; then
            log "Generating self-signed SSL certificates..."
            openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
                -keyout ssl/your-domain.key \
                -out ssl/your-domain.crt \
                -subj "/C=US/ST=State/L=City/O=Organization/OU=OrgUnit/CN=localhost"
            log "Self-signed certificates generated"
        else
            warn "SSL certificates required for HTTPS. Place them in ssl/ directory."
        fi
    fi
}

# Setup directories
setup_directories() {
    log "Setting up required directories..."
    
    mkdir -p logs/nginx
    mkdir -p backups
    mkdir -p media
    
    # Set proper permissions
    chmod 755 logs backups media
    chmod 755 logs/nginx
}

# Build and deploy
deploy() {
    log "Starting deployment..."
    
    # Stop existing containers
    log "Stopping existing containers..."
    docker-compose -f production-deploy.yml down || true
    
    # Build images
    log "Building Docker images..."
    docker-compose -f production-deploy.yml build
    
    # Start services
    log "Starting services..."
    docker-compose -f production-deploy.yml up -d
    
    # Wait for services to be ready
    log "Waiting for services to start..."
    sleep 30
    
    # Run migrations
    log "Running database migrations..."
    docker-compose -f production-deploy.yml exec -T web python manage.py migrate
    
    # Collect static files
    log "Collecting static files..."
    docker-compose -f production-deploy.yml exec -T web python manage.py collectstatic --noinput
    
    # Create superuser if needed
    log "Checking for superuser..."
    if ! docker-compose -f production-deploy.yml exec -T web python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); print('exists' if User.objects.filter(is_superuser=True).exists() else 'none')"; then
        log "Creating superuser..."
        docker-compose -f production-deploy.yml exec web python manage.py createsuperuser
    fi
}

# Health check
health_check() {
    log "Performing health check..."
    
    # Check if containers are running
    if ! docker-compose -f production-deploy.yml ps | grep "Up" > /dev/null; then
        error "Some containers are not running properly"
    fi
    
    # Check web service health
    for i in {1..30}; do
        if curl -f http://localhost:8000/health/ > /dev/null 2>&1; then
            log "Web service is healthy"
            break
        fi
        if [[ $i -eq 30 ]]; then
            error "Web service health check failed after 30 attempts"
        fi
        log "Waiting for web service to be ready... (attempt $i/30)"
        sleep 2
    done
    
    # Check nginx
    if curl -f http://localhost:8080/ > /dev/null 2>&1; then
        log "Nginx intranet access is working"
    else
        warn "Nginx intranet access may not be working properly"
    fi
}

# Display access information
show_access_info() {
    log "Deployment completed successfully!"
    echo
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}                    ACCESS INFORMATION                          ${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
    echo
    echo -e "${GREEN}🌐 Internet Access:${NC}"
    echo "   - HTTPS: https://your-domain.com"
    echo "   - HTTP:  http://your-domain.com (redirects to HTTPS)"
    echo
    echo -e "${GREEN}🏠 Intranet Access:${NC}"
    echo "   - Direct: http://localhost:8080"
    echo "   - Internal IPs only (192.168.x.x, 10.x.x.x, 172.16-31.x.x)"
    echo
    echo -e "${GREEN}🔧 Admin Interface:${NC}"
    echo "   - Admin: https://your-domain.com/admin/"
    echo "   - API:   https://your-domain.com/api/"
    echo
    echo -e "${GREEN}📊 Current Database State:${NC}"
    TOTAL_CUSTOMERS=$(docker-compose -f production-deploy.yml exec -T web python manage.py shell -c "from crm.models import Customer; print(Customer.objects.count())")
    YOUTUBE_CUSTOMERS=$(docker-compose -f production-deploy.yml exec -T web python manage.py shell -c "from crm.models import Customer; print(Customer.objects.filter(customer_type='youtuber').count())")
    REGULAR_CUSTOMERS=$((TOTAL_CUSTOMERS - YOUTUBE_CUSTOMERS))
    
    echo "   - Total Customers: $TOTAL_CUSTOMERS"
    echo "   - Regular Customers: $REGULAR_CUSTOMERS"
    echo "   - YouTube Creators: $YOUTUBE_CUSTOMERS"
    echo
    echo -e "${YELLOW}📋 Next Steps:${NC}"
    echo "   1. Update your domain DNS to point to this server"
    echo "   2. Replace self-signed SSL certificates with real ones"
    echo "   3. Update .env.production with production values"
    echo "   4. Configure firewall to allow ports 80, 443, and 8080"
    echo "   5. Set up regular backups using: docker-compose -f production-deploy.yml run backup"
    echo
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
}

# Main execution
main() {
    log "Starting CRM System Production Deployment"
    
    check_root
    check_prerequisites
    setup_environment
    setup_ssl
    setup_directories
    deploy
    health_check
    show_access_info
}

# Run main function
main "$@"
