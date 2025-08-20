#!/bin/bash

# Firewall Configuration Script for CRM Port 8082
# This script configures UFW to allow external access to the CRM system

echo "=================================================="
echo "    CRM FIREWALL CONFIGURATION"
echo "    Opening port 8082 for internet access"
echo "=================================================="

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running with appropriate permissions
if ! sudo -n true 2>/dev/null; then
    error "This script requires sudo privileges to configure the firewall."
    echo ""
    echo "Please run with sudo or ensure you have sudo access:"
    echo "  sudo ./configure_firewall.sh"
    echo ""
    echo "Or run the commands manually:"
    echo "  sudo ufw status"
    echo "  sudo ufw allow 8082/tcp"
    echo "  sudo ufw reload"
    exit 1
fi

# Check current firewall status
log "Checking current firewall status..."
sudo ufw status

echo ""
log "Configuring firewall for CRM access..."

# Enable UFW if not already enabled
if ! sudo ufw status | grep -q "Status: active"; then
    warn "UFW is not active. Enabling UFW..."
    sudo ufw --force enable
fi

# Add rule for port 8082
log "Adding rule for port 8082..."
sudo ufw allow 8082/tcp comment "CRM System HTTP Access"

# Add rule for SSH to ensure we don't lock ourselves out
log "Ensuring SSH access is allowed..."
sudo ufw allow ssh

# Reload firewall rules
log "Reloading firewall rules..."
sudo ufw reload

echo ""
log "Firewall configuration complete!"

# Show final status
echo ""
echo "Final firewall status:"
sudo ufw status numbered

echo ""
echo "=================================================="
echo "    FIREWALL CONFIGURATION COMPLETE"
echo "=================================================="
echo ""
echo "✅ Port 8082 is now open for external access"
echo "🌐 Your CRM should be accessible at:"
echo "   http://203.186.246.162:8082/"
echo "🔑 Admin panel:"
echo "   http://203.186.246.162:8082/admin/"
echo ""
echo "🔒 Security notes:"
echo "   • SSH access is maintained for server management"
echo "   • Only port 8082 is opened for CRM access"
echo "   • Consider using HTTPS in production"
echo ""
echo "📝 To test external access:"
echo "   Open http://203.186.246.162:8082/ in your browser"
echo ""
