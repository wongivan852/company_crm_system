# Generated migration for making names optional for YouTubers

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("crm", "0014_make_email_optional_for_youtubers"),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='first_name',
            field=models.CharField(blank=True, help_text='Given name/First name', max_length=100),
        ),
        migrations.AlterField(
            model_name='customer',
            name='last_name',
            field=models.CharField(blank=True, help_text='Family name/Last name/Surname', max_length=100),
        ),
    ]