# 🚀 CRM Deployment Guide - MacBook Testing to Ubuntu Production

## **PHASE 1: Multi-Device Testing on MacBook (READY NOW)**

### **🔧 Quick Start - Testing on Your Network**

1. **Start the testing server:**
   ```bash
   cd /Users/wongivan/company_crm_system
   ./start_testing_server.sh
   ```

2. **Access from other devices:**
   - **Local MacBook**: http://localhost:8000
   - **Network devices**: http://192.168.0.164:8000
   - **Alternative IP**: http://10.5.0.2:8000

3. **Key Testing URLs:**
   - **Admin Panel**: `/admin/`
   - **API Root**: `/api/v1/`
   - **UAT Dashboard**: `/dashboard/`
   - **Customer List**: `/customers/`

### **📱 Testing Features**

#### **Cross-Device API Testing**
- **CORS enabled** for all origins during testing
- **API endpoints** accessible from mobile/tablet browsers
- **Admin interface** works on all devices
- **File uploads** supported across devices

#### **UAT Access**
- **UAT Token**: `test-access-token-123`
- **Public views enabled** for testing
- **Relaxed security** for development convenience

### **🔒 Security Settings (Testing Mode)**
- `DEBUG = True` (detailed error pages)
- `CORS_ALLOW_ALL_ORIGINS = True` 
- SSL redirect disabled for HTTP testing
- Reduced authentication requirements for UAT views

---

## **PHASE 2: Ubuntu Server Production Deployment**

### **🏗️ Server Preparation**

#### **1. Run Initial Setup (as root/sudo):**
```bash
# On Ubuntu server
curl -o ubuntu_setup.sh https://your-repo/deploy/ubuntu_setup.sh
chmod +x ubuntu_setup.sh
sudo ./ubuntu_setup.sh
```

#### **2. What the setup script does:**
- Installs **Python 3, PostgreSQL, Redis, Nginx**
- Creates **`crmuser`** system user
- Configures **firewall** (ports 80, 443, 8000)
- Sets up **application directories**
- Configures **Supervisor** for process management
- Creates **Nginx configuration**

### **🚀 Application Deployment**

#### **1. Switch to application user:**
```bash
sudo su - crmuser
cd /opt/crm
```

#### **2. Clone your repository:**
```bash
git clone https://github.com/your-username/crm_project.git .
```

#### **3. Run deployment script:**
```bash
./deploy/deploy.sh
```

### **⚙️ Production Configuration**

#### **1. Update environment variables in `.env`:**
```bash
# Critical settings to change
SECRET_KEY=your-super-secret-production-key
ALLOWED_HOSTS=your-domain.com,your-server-ip
DEBUG=False

# Database
DB_NAME=crm_production
DB_USER=crm_user
DB_PASSWORD=your-secure-password

# Email
EMAIL_HOST_USER=your-email@domain.com
EMAIL_HOST_PASSWORD=your-app-password
```

#### **2. Configure your domain in Nginx:**
```bash
sudo nano /etc/nginx/sites-available/crm
# Update: server_name your-domain.com www.your-domain.com;
sudo nginx -t && sudo systemctl restart nginx
```

#### **3. Set up SSL certificate:**
```bash
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

---

## **🌐 Network Architecture**

### **Testing Phase (MacBook)**
```
[Mobile Device] ──→ [WiFi Router] ──→ [MacBook:8000] ──→ [Django Dev Server]
     192.168.0.x         LAN           192.168.0.164      SQLite + Redis
```

### **Production Phase (Ubuntu)**
```
[Internet] ──→ [Domain/IP] ──→ [Nginx:80/443] ──→ [Gunicorn] ──→ [Django App]
                                   ↓                           ↓
                              [SSL/TLS]                 [PostgreSQL + Redis]
```

---

## **🔧 Service Management**

### **Development (MacBook)**
```bash
# Start testing server
./start_testing_server.sh

# Stop server: Ctrl+C
```

### **Production (Ubuntu)**
```bash
# Check status
sudo supervisorctl status

# Restart services
sudo supervisorctl restart crm
sudo supervisorctl restart crm-celery
sudo systemctl restart nginx

# View logs
sudo tail -f /var/log/crm/gunicorn.log
sudo tail -f /var/log/crm/celery.log
```

---

## **📊 Performance & Monitoring**

### **Testing Metrics**
- **Page Load**: Target < 2 seconds on local network
- **API Response**: Target < 500ms
- **Multi-device compatibility**: iOS, Android, Windows

### **Production Monitoring**
```bash
# Performance logs
sudo tail -f /var/log/crm/performance.log

# System resources
htop
sudo systemctl status crm
```

---

## **🔄 Update Workflow**

### **Development Updates**
1. Test changes locally: `./start_testing_server.sh`
2. Test on multiple devices
3. Commit and push to repository

### **Production Updates**
```bash
# On Ubuntu server as crmuser
cd /opt/crm
git pull origin main
./deploy/deploy.sh
```

---

## **🚨 Troubleshooting**

### **Common Testing Issues**

#### **Device can't connect:**
```bash
# Check MacBook firewall
sudo pfctl -sr | grep 8000

# Check Django server is binding to 0.0.0.0:8000
netstat -an | grep 8000
```

#### **CORS errors:**
- Verify `CORS_ALLOW_ALL_ORIGINS=True` in `.env.testing`
- Check browser console for specific CORS errors

### **Production Issues**

#### **502 Bad Gateway:**
```bash
# Check Gunicorn status
sudo supervisorctl status crm

# Check Nginx configuration
sudo nginx -t

# Check logs
sudo tail -f /var/log/crm/gunicorn.log
```

#### **Database connection errors:**
```bash
# Check PostgreSQL
sudo systemctl status postgresql

# Test database connection
sudo -u postgres psql crm_production
```

---

## **📋 Deployment Checklist**

### **✅ Testing Phase (MacBook)**
- [x] Testing server script created
- [x] Network accessibility configured
- [x] CORS enabled for multi-device access
- [x] UAT views enabled
- [x] Performance optimizations applied

### **⚡ Production Phase (Ubuntu)**
- [ ] Ubuntu server setup completed
- [ ] Domain name configured
- [ ] SSL certificate installed
- [ ] Database secured
- [ ] Email service configured
- [ ] Backup strategy implemented
- [ ] Monitoring configured

---

## **🎯 Ready for Testing!**

Your CRM is now configured for multi-device testing on your MacBook. Run:

```bash
./start_testing_server.sh
```

Access from any device on your network at:
- **http://192.168.0.164:8000**

For production deployment on Ubuntu server, follow Phase 2 instructions above.

**🚀 Happy testing and deploying!**