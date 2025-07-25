# Generated manually to add address field
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0006_customer_city_customer_postal_code_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='address',
            field=models.CharField(blank=True, help_text='Street address', max_length=500),
        ),
    ]
