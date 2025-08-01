# Generated migration for making email optional for YouTubers

from django.db import migrations, models
from django.core.validators import EmailValidator


class Migration(migrations.Migration):
    dependencies = [
        ("crm", "0013_add_youtube_fields"),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_type',
            field=models.CharField(choices=[('individual', 'Individual Learner'), ('corporate', 'Corporate Client'), ('student', 'Student'), ('instructor', 'Instructor'), ('youtuber', 'YouTuber/Content Creator')], max_length=20),
        ),
        migrations.AlterField(
            model_name='customer',
            name='email_primary',
            field=models.EmailField(blank=True, help_text='Primary email address', max_length=254, null=True, validators=[EmailValidator()]),
        ),
    ]