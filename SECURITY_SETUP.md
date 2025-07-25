# Security Setup Guide

## 🔒 Critical Security Configuration

### 1. Environment Variables Setup

**Development:**
```bash
cp .env.example crm_project/.env
# Edit .env with your development credentials
```

**Production:**
```bash
cp .env.production.example .env.production
# Edit .env.production with secure production credentials
```

### 2. Generate Secure SECRET_KEY

```python
# Run in Django shell or Python console
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### 3. Database Security

**Create Secure Database User:**
```sql
-- Connect to PostgreSQL as superuser
CREATE USER crm_prod_user WITH PASSWORD 'your_strong_password_here';
CREATE DATABASE crm_production_db OWNER crm_prod_user;

-- Grant minimal required permissions
GRANT CONNECT ON DATABASE crm_production_db TO crm_prod_user;
GRANT USAGE ON SCHEMA public TO crm_prod_user;
GRANT CREATE ON SCHEMA public TO crm_prod_user;
```

**Database Password Requirements:**
- Minimum 12 characters
- Mix of uppercase, lowercase, numbers, and symbols
- No dictionary words
- Example: `X9$mK2#vR8@nQ5!pL7`

### 4. SSL/HTTPS Configuration

**Production Settings:**
- Set `SECURE_SSL_REDIRECT=True`
- Configure reverse proxy (nginx/Apache) for SSL termination
- Use Let's Encrypt or commercial SSL certificate

### 5. API Keys Security

**Never commit these to version control:**
- WhatsApp API tokens
- WeChat credentials
- Email service passwords
- Database passwords
- SECRET_KEY

### 6. File Permissions

**Set proper file permissions:**
```bash
chmod 600 .env
chmod 600 .env.production
chmod 755 manage.py
```

### 7. Firewall Configuration

**Database Server:**
- Only allow connections from application server
- Block direct internet access to database
- Use VPC/private networking if possible

**Application Server:**
- Only open ports 80 and 443
- Close all unnecessary ports
- Use fail2ban for brute force protection

### 8. Regular Security Updates

```bash
# Update dependencies regularly
pip list --outdated
pip install -U package_name

# Check for security vulnerabilities
pip-audit
```

### 9. Backup Security

- Encrypt database backups
- Store backups in secure location
- Test backup restoration regularly
- Implement backup retention policy

### 10. Monitoring

- Monitor failed login attempts
- Set up alerts for unusual database activity
- Log all admin actions
- Monitor file system changes

## ⚠️ Security Checklist

- [ ] SECRET_KEY moved to environment variable
- [ ] DEBUG=False in production
- [ ] Strong database password set
- [ ] SSL/HTTPS configured
- [ ] API keys secured
- [ ] File permissions set correctly
- [ ] Firewall configured
- [ ] Regular security updates scheduled
- [ ] Backup encryption enabled
- [ ] Monitoring configured

## 🚨 Immediate Actions Required

1. **Change default database password** (currently empty)
2. **Set up SSL certificate** for production
3. **Configure email service** with proper credentials
4. **Set up monitoring** and alerting
5. **Create backup strategy**

## 📞 Emergency Contacts

- System Administrator: [Your contact]
- Database Administrator: [Your contact]
- Security Team: [Your contact]