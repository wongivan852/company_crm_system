# management/commands/load_sample_data.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from crm.models import Customer, Course, Conference, Enrollment
import random

class Command(BaseCommand):
    help = 'Load sample data for testing the CRM system'

    def add_arguments(self, parser):
        parser.add_argument(
            '--customers',
            type=int,
            default=50,
            help='Number of sample customers to create'
        )
        parser.add_argument(
            '--courses',
            type=int,
            default=10,
            help='Number of sample courses to create'
        )

    def handle(self, *args, **options):
        self.stdout.write('Loading sample data...')
        
        customers_count = options['customers']
        courses_count = options['courses']
        
        self.create_sample_customers(customers_count)
        self.create_sample_courses(courses_count)
        self.create_sample_conferences()
        self.create_sample_enrollments()
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully loaded sample data: '
                f'{customers_count} customers, {courses_count} courses'
            )
        )

    def create_sample_customers(self, count):
        sample_customers = [
            {
                'first_name': 'Alice',
                'last_name': 'Johnson',
                'email': 'alice.johnson@email.com',
                'phone': '+1234567890',
                'whatsapp_number': '+1234567890',
                'customer_type': 'individual',
                'status': 'active',
                'company': 'Tech Corp',
                'position': 'Software Engineer',
                'preferred_communication': 'email',
                'interests': 'Python, Data Science, Machine Learning'
            },
            {
                'first_name': 'Bob',
                'last_name': 'Smith',
                'email': 'bob.smith@email.com',
                'phone': '+1234567891',
                'whatsapp_number': '+1234567891',
                'customer_type': 'corporate',
                'status': 'active',
                'company': 'Innovation Inc',
                'position': 'CTO',
                'preferred_communication': 'whatsapp',
                'interests': 'Leadership, Technology Strategy'
            },
        ]
        
        # Create base customers
        for customer_data in sample_customers:
            customer, created = Customer.objects.get_or_create(
                email=customer_data['email'],
                defaults=customer_data
            )
            if created:
                self.stdout.write(f'Created customer: {customer.first_name} {customer.last_name}')

    def create_sample_courses(self, count):
        sample_courses = [
            {
                'title': 'Python Programming Bootcamp',
                'description': 'Comprehensive Python programming course',
                'course_type': 'online',
                'duration_hours': 40,
                'price': 299.00,
                'max_participants': 30,
                'start_date': timezone.now() + timedelta(days=30),
                'end_date': timezone.now() + timedelta(days=45),
                'registration_deadline': timezone.now() + timedelta(days=25)
            },
        ]
        
        for course_data in sample_courses:
            course, created = Course.objects.get_or_create(
                title=course_data['title'],
                defaults=course_data
            )
            if created:
                self.stdout.write(f'Created course: {course.title}')

    def create_sample_conferences(self):
        pass  # Implementation similar to courses

    def create_sample_enrollments(self):
        pass  # Implementation to create sample enrollments
