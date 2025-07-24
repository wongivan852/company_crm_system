# Learning Institute CRM System

A comprehensive Customer Relationship Management system designed specifically for learning institutes, featuring multi-channel communication capabilities and complete student lifecycle management.

## 🎓 Overview

This CRM system provides a complete solution for managing customers (students), courses, conferences, and multi-channel communications for educational institutions.

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

## 📦 Installation

### Prerequisites
- Python 3.8+
- PostgreSQL
- Redis (for Celery tasks)

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd company_crm_system
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install django djangorestframework django-filter django-cors-headers
   pip install psycopg2-binary celery redis python-decouple
   ```

4. **Configure database**
   - Create PostgreSQL database: `crm_db`
   - Update database settings in `settings.py`

5. **Run migrations**
   ```bash
   cd crm_project
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Load sample data**
   ```bash
   python manage.py load_sample_data
   ```

8. **Start development server**
   ```bash
   python manage.py runserver
   ```

## 🌐 Usage

### Web Interface
- **Dashboard**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **API Root**: http://127.0.0.1:8000/api/

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

## 🚀 Deployment

For production deployment:
1. Set `DEBUG = False` in settings
2. Configure proper database credentials
3. Set up environment variables for API keys
4. Configure static file serving
5. Set up SSL certificates
6. Configure Celery with proper broker

---

**Built with ❤️ for Learning Institutes**
