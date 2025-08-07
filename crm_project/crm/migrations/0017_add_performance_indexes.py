# Add performance indexes migration
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0001_initial'),
    ]

    operations = [
        # Customer model indexes
        migrations.RunSQL(
            "CREATE INDEX IF NOT EXISTS crm_customer_email_primary_idx ON crm_customer(email_primary);",
            reverse_sql="DROP INDEX IF EXISTS crm_customer_email_primary_idx;"
        ),
        migrations.RunSQL(
            "CREATE INDEX IF NOT EXISTS crm_customer_type_status_idx ON crm_customer(customer_type, status);",
            reverse_sql="DROP INDEX IF EXISTS crm_customer_type_status_idx;"
        ),
        migrations.RunSQL(
            "CREATE INDEX IF NOT EXISTS crm_customer_country_region_idx ON crm_customer(country_region);",
            reverse_sql="DROP INDEX IF EXISTS crm_customer_country_region_idx;"
        ),
        migrations.RunSQL(
            "CREATE INDEX IF NOT EXISTS crm_customer_source_idx ON crm_customer(source);",
            reverse_sql="DROP INDEX IF EXISTS crm_customer_source_idx;"
        ),
        migrations.RunSQL(
            "CREATE INDEX IF NOT EXISTS crm_customer_phone_primary_idx ON crm_customer(phone_primary);",
            reverse_sql="DROP INDEX IF EXISTS crm_customer_phone_primary_idx;"
        ),
        migrations.RunSQL(
            "CREATE INDEX IF NOT EXISTS crm_customer_whatsapp_idx ON crm_customer(whatsapp_number);",
            reverse_sql="DROP INDEX IF EXISTS crm_customer_whatsapp_idx;"
        ),
        migrations.RunSQL(
            "CREATE INDEX IF NOT EXISTS crm_customer_youtube_handle_idx ON crm_customer(youtube_handle);",
            reverse_sql="DROP INDEX IF EXISTS crm_customer_youtube_handle_idx;"
        ),
        migrations.RunSQL(
            "CREATE INDEX IF NOT EXISTS crm_customer_created_status_idx ON crm_customer(created_at, status);",
            reverse_sql="DROP INDEX IF EXISTS crm_customer_created_status_idx;"
        ),
        
        # Enrollment model indexes
        migrations.RunSQL(
            "CREATE INDEX IF NOT EXISTS crm_enrollment_customer_status_idx ON crm_enrollment(customer_id, status);",
            reverse_sql="DROP INDEX IF EXISTS crm_enrollment_customer_status_idx;"
        ),
        migrations.RunSQL(
            "CREATE INDEX IF NOT EXISTS crm_enrollment_date_idx ON crm_enrollment(enrollment_date);",
            reverse_sql="DROP INDEX IF EXISTS crm_enrollment_date_idx;"
        ),
        migrations.RunSQL(
            "CREATE INDEX IF NOT EXISTS crm_enrollment_payment_status_idx ON crm_enrollment(payment_status);",
            reverse_sql="DROP INDEX IF EXISTS crm_enrollment_payment_status_idx;"
        ),
        
        # Course model indexes
        migrations.RunSQL(
            "CREATE INDEX IF NOT EXISTS crm_course_type_active_idx ON crm_course(course_type, is_active);",
            reverse_sql="DROP INDEX IF EXISTS crm_course_type_active_idx;"
        ),
        migrations.RunSQL(
            "CREATE INDEX IF NOT EXISTS crm_course_start_date_idx ON crm_course(start_date);",
            reverse_sql="DROP INDEX IF EXISTS crm_course_start_date_idx;"
        ),
        migrations.RunSQL(
            "CREATE INDEX IF NOT EXISTS crm_course_active_start_idx ON crm_course(is_active, start_date);",
            reverse_sql="DROP INDEX IF EXISTS crm_course_active_start_idx;"
        ),
        
        # CommunicationLog model indexes
        migrations.RunSQL(
            "CREATE INDEX IF NOT EXISTS crm_comm_log_customer_channel_idx ON crm_communicationlog(customer_id, channel);",
            reverse_sql="DROP INDEX IF EXISTS crm_comm_log_customer_channel_idx;"
        ),
        migrations.RunSQL(
            "CREATE INDEX IF NOT EXISTS crm_comm_log_sent_at_idx ON crm_communicationlog(sent_at);",
            reverse_sql="DROP INDEX IF EXISTS crm_comm_log_sent_at_idx;"
        ),
        migrations.RunSQL(
            "CREATE INDEX IF NOT EXISTS crm_comm_log_channel_sent_idx ON crm_communicationlog(channel, sent_at);",
            reverse_sql="DROP INDEX IF EXISTS crm_comm_log_channel_sent_idx;"
        ),
        
        # Conference model indexes
        migrations.RunSQL(
            "CREATE INDEX IF NOT EXISTS crm_conference_active_start_idx ON crm_conference(is_active, start_date);",
            reverse_sql="DROP INDEX IF EXISTS crm_conference_active_start_idx;"
        ),
        
        # YouTubeMessage model indexes (already have some from existing model)
        migrations.RunSQL(
            "CREATE INDEX IF NOT EXISTS crm_youtube_message_status_idx ON crm_youtubemessage(status);",
            reverse_sql="DROP INDEX IF EXISTS crm_youtube_message_status_idx;"
        ),
    ]