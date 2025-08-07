# Learning Institute CRM System - UAT v1.0

A comprehensive Customer Relationship Management system designed specifically for learning institutes, featuring multi-channel communication capabilities and complete student lifecycle management.

## 🎓 Overview

This CRM system provides a complete solution for managing customers (students), courses, conferences, and multi-channel communications for educational institutions. Currently deployed for User Acceptance Testing (UAT) with both virtual environment and Docker containerization support.

## ✨ Features

### Core Functionality
- **Customer Management** - Complete CRUD operations for student data
- **Course Administration** - Manage course offerings, schedules, and pricing
- **Conference Management** - Event planning and attendee management
- **Enrollment Tracking** - Student course registration and status management

### Multi-Channel Communication
- **WhatsApp Business API** - Direct messaging to students
- **Email Integration** - SMTP-based email communications
- **WeChat Corporate API** - Messaging for international students
- **Communication Logging** - Complete audit trail of all interactions

### Technical Features
- **REST API** - Complete API for integrations
- **Admin Interface** - Django admin for power users
- **Responsive Web UI** - Bootstrap-based user interface
- **Background Tasks** - Celery integration for bulk operations
- **Search & Filtering** - Advanced data filtering capabilities

## 🚀 Technology Stack

- **Backend**: Django 4.2.5
- **Database**: PostgreSQL
- **API**: Django REST Framework
- **Frontend**: Bootstrap 5
- **Task Queue**: Celery + Redis
- **Communication**: WhatsApp, Email, WeChat APIs

## 📦 Installation & Deployment

### 🚀 Quick Start (UAT Environment)

**Current UAT Deployment is LIVE at:**
- **🏢 Main Application**: `http://192.168.0.104:8082/`
- **👤 Admin Panel**: `http://192.168.0.104:8082/admin/`
- **🧪 Network Test**: `http://192.168.0.104:8082/network-test/`
- **🎨 Landing Page**: `http://192.168.0.104:8082/network-landing/`

**Admin Credentials:**
- Username: `admin`
- Password: `admin123`

### 🐍 Development Environment (Current Setup)

**Virtual Environment Configuration:**
```bash
# Using existing virtual environment
source /home/user/krystal-company-apps/claude-env/bin/activate

# Start development server
cd crm_project
python manage.py runserver 0.0.0.0:8082
```

**Environment Details:**
- Python: 3.12.3
- Virtual Environment: `/home/user/krystal-company-apps/claude-env/`
- Database: SQLite (development)
- Network: Accessible from WiFi devices (192.168.0.104:8082)

### 🐳 Docker Production Environment

**Full containerized stack available:**
```bash
# Start all services
docker-compose up -d

# Services included:
# - PostgreSQL database (port 5432)
# - Redis cache (port 6379)
# - Django application (port 8000)
# - Celery workers
# - Celery beat scheduler
```

### Prerequisites
- Python 3.8+
- PostgreSQL
- Redis (for Celery tasks)

### Setup

#### Option 1: Use Existing Environment (Recommended for UAT)
```bash
# Clone and navigate
git clone <repository-url>
cd company_crm_system

# Use existing virtual environment
source /home/user/krystal-company-apps/claude-env/bin/activate

# Apply migrations (if needed)
cd crm_project
python manage.py migrate

# Start server
python manage.py runserver 0.0.0.0:8082
```

#### Option 2: Fresh Installation
#### Option 2: Fresh Installation
```bash
# 1. Clone the repository
git clone <repository-url>
cd company_crm_system

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup database and run migrations
cd crm_project
python manage.py migrate

# 5. Create superuser
python manage.py createsuperuser

# 6. Start development server
python manage.py runserver 0.0.0.0:8082
```

#### Option 3: Docker Deployment
```bash
# Build and start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f web
```

## 🌐 UAT Access Information

### Network Configuration
- **Server IP**: 192.168.0.104
- **WiFi Network**: Krystal-414-b
- **Port**: 8082
- **Firewall**: Configured for external device access
- **Protocol**: HTTP (development mode)

### Testing Endpoints
- **Health Check**: GET `/network-test/` - Returns JSON status
- **Landing Page**: GET `/network-landing/` - Interactive test page
- **Admin Login**: POST `/admin/` - Django admin interface
- **API Root**: GET `/api/` - REST API endpoints

## 🌐 Usage

### UAT Environment Access
- **Dashboard**: http://192.168.0.104:8082/
- **Admin Panel**: http://192.168.0.104:8082/admin/
- **API Root**: http://192.168.0.104:8082/api/
- **Network Test**: http://192.168.0.104:8082/network-test/

### Local Development
- **Dashboard**: http://127.0.0.1:8082/
- **Admin Panel**: http://127.0.0.1:8082/admin/
- **API Root**: http://127.0.0.1:8082/api/

### API Endpoints

#### Customers
- `GET /api/customers/` - List all customers
- `POST /api/customers/` - Create new customer
- `GET /api/customers/{id}/` - Get customer details
- `PUT /api/customers/{id}/` - Update customer
- `DELETE /api/customers/{id}/` - Delete customer

#### Courses
- `GET /api/courses/` - List all courses
- `POST /api/courses/` - Create new course
- `GET /api/courses/{id}/enroll/` - Enroll customer in course

#### Communication
- `POST /api/customers/{id}/send_message/` - Send message to customer

## ⚙️ Configuration

### Communication APIs

#### WhatsApp Business API
```python
WHATSAPP_API_URL = 'https://graph.facebook.com/v18.0'
WHATSAPP_ACCESS_TOKEN = 'your-access-token'
WHATSAPP_PHONE_NUMBER_ID = 'your-phone-number-id'
```

#### Email Configuration
```python
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

#### WeChat Corporate API
```python
WECHAT_CORP_ID = 'your-corp-id'
WECHAT_CORP_SECRET = 'your-corp-secret'
WECHAT_AGENT_ID = 'your-agent-id'
```

## 📊 Data Models

### Customer
- Personal information (name, email, phone)
- Communication preferences
- Marketing consent
- Company and occupation details

### Course
- Course details (title, description, duration)
- Pricing and capacity
- Instructor and category information
- Schedule and status

### Conference
- Event information
- Location and capacity
- Speaker lineup and agenda
- Pricing and registration

### Enrollment
- Customer-course relationships
- Enrollment status tracking
- Registration timestamps

## 🔧 Development

### Background Tasks
The system uses Celery for background task processing:

```bash
# Start Celery worker
celery -A crm_project worker --loglevel=info

# Start Celery beat (for scheduled tasks)
celery -A crm_project beat --loglevel=info
```

### Testing
```bash
python manage.py test
```

### Code Quality
- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Write comprehensive tests
- Document complex functions

## 📁 Project Structure

```
company_crm_system/
├── crm_project/
│   ├── manage.py
│   ├── crm_project/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── celery.py
│   └── crm/
│       ├── models.py
│       ├── views.py
│       ├── serializers.py
│       ├── forms.py
│       ├── urls.py
│       ├── admin.py
│       ├── communication_services.py
│       ├── tasks.py
│       ├── templates/
│       └── management/
│           └── commands/
├── .gitignore
└── README.md
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Email: info@learninginstitute.com
- Phone: +1234567890

## 🚀 UAT Deployment Status

### Environment Information
- **Version**: UAT v1.0
- **Deployment Date**: August 6, 2025
- **Environment Type**: Development with Network Access
- **Database**: SQLite (264KB)
- **Server**: Django Development Server
- **Network**: WiFi accessible (192.168.0.104:8082)

### Architecture
```
UAT Environment:
┌─────────────────────────────────────────┐
│ Host System (192.168.0.104)            │
│ ┌─────────────────────────────────────┐ │
│ │ Virtual Environment (claude-env)    │ │
│ │ ├─ Python 3.12.3                   │ │
│ │ ├─ Django 4.2.16                   │ │
│ │ ├─ SQLite Database                 │ │
│ │ └─ Development Server :8082        │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ Docker (Available):                     │
│ ├─ PostgreSQL Container                 │
│ ├─ Redis Container                      │
│ ├─ Django Container :8000              │
│ ├─ Celery Worker                       │
│ └─ Celery Beat Scheduler               │
└─────────────────────────────────────────┘
```

### Network Configuration
- **Firewall**: Configured for ICMP ping and port 8082
- **Binding**: 0.0.0.0:8082 (accepts external connections)
- **Gateway**: 192.168.0.1 (accessible)
- **WiFi**: Krystal-414-b network

## 🚀 Deployment

For production deployment:
1. Set `DEBUG = False` in settings
2. Configure proper database credentials
3. Set up environment variables for API keys
4. Configure static file serving
5. Set up SSL certificates
6. Configure Celery with proper broker

---

## 📝 Version History

### UAT v1.0 (August 6, 2025)
- ✅ Complete CRM system setup with virtual environment
- ✅ Network accessibility configured (192.168.0.104:8082)
- ✅ Admin panel with fresh database (admin/admin123)
- ✅ Docker containerization support available
- ✅ Multi-device WiFi access enabled
- ✅ Network diagnostic tools implemented
- ✅ Landing page for connectivity testing
- ✅ RESTful API endpoints functional
- 🔧 Environment: Python 3.12.3 + Django 4.2.16
- 🔧 Database: SQLite (development), PostgreSQL (production ready)
- 🔧 Deployment: Virtual environment (active), Docker (available)

**Built with ❤️ for Learning Institutes - UAT Ready!**
