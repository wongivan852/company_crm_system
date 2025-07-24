#!/bin/bash

# setup.sh - Setup script for Learning Institute CRM
echo "🎓 Setting up Learning Institute CRM System..."

# Check if PostgreSQL is running
echo "📊 Checking PostgreSQL status..."
if ! pg_isready > /dev/null 2>&1; then
    echo "⚠️  PostgreSQL is not running. Starting it..."
    brew services start postgresql@14
    sleep 3
fi

# Navigate to project directory
cd crm_project

# Create logs directory
echo "📁 Creating logs directory..."
mkdir -p logs

# Create and run migrations
echo "🔧 Creating and applying database migrations..."
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
echo "👤 Creating superuser account..."
echo "Please create an admin account:"
python manage.py createsuperuser

# Load sample data
echo "📝 Loading sample data..."
python manage.py load_sample_data --customers 25 --courses 8

# Collect static files (for production)
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

echo "✅ Setup completed successfully!"
echo ""
echo "🚀 You can now:"
echo "   • Start the development server: python manage.py runserver"
echo "   • Access the web interface: http://localhost:8000"
echo "   • Access the admin interface: http://localhost:8000/admin"
echo "   • Explore the API: http://localhost:8000/api/v1/"
echo ""
echo "🔧 Optional services:"
echo "   • Start Redis: brew services start redis"
echo "   • Start Celery worker: celery -A crm_project worker --loglevel=info"
echo "   • Start Celery beat: celery -A crm_project beat --loglevel=info"
