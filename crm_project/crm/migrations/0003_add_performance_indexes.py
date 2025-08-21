# Generated performance indexes migration for CRM system
from django.db import migrations, models

class Migration(migrations.Migration):
    
    dependencies = [
        ('crm', '0002_enhanced_models_and_performance'),  # Adjust based on your latest migration
    ]
    
    operations = [
        # Customer performance indexes
        migrations.RunSQL(
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_customer_search_fulltext ON crm_customer USING gin(to_tsvector('english', coalesce(first_name, '') || ' ' || coalesce(last_name, '') || ' ' || coalesce(email_primary, '') || ' ' || coalesce(company_primary, '')));",
            reverse_sql="DROP INDEX IF EXISTS idx_customer_search_fulltext;"
        ),
        migrations.RunSQL(
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_customer_email_lower ON crm_customer USING btree(lower(email_primary));",
            reverse_sql="DROP INDEX IF EXISTS idx_customer_email_lower;"
        ),
        migrations.RunSQL(
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_customer_phone_clean ON crm_customer USING btree(regexp_replace(phone_primary, '[^0-9]', '', 'g')) WHERE phone_primary IS NOT NULL;",
            reverse_sql="DROP INDEX IF EXISTS idx_customer_phone_clean;"
        ),
        migrations.RunSQL(
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_customer_active_created ON crm_customer (created_at DESC, status) WHERE status = 'active';",
            reverse_sql="DROP INDEX IF EXISTS idx_customer_active_created;"
        ),
        migrations.RunSQL(
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_customer_company_active ON crm_customer (company_primary, status) WHERE company_primary IS NOT NULL AND company_primary != '';",
            reverse_sql="DROP INDEX IF EXISTS idx_customer_company_active;"
        ),
        
        # Communication log performance indexes
        migrations.RunSQL(
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_communication_recent ON crm_communicationlog (sent_at DESC, channel, is_outbound) WHERE sent_at >= CURRENT_DATE - INTERVAL '30 days';",
            reverse_sql="DROP INDEX IF EXISTS idx_communication_recent;"
        ),
        migrations.RunSQL(
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_communication_customer_recent ON crm_communicationlog (customer_id, sent_at DESC) WHERE sent_at >= CURRENT_DATE - INTERVAL '90 days';",
            reverse_sql="DROP INDEX IF EXISTS idx_communication_customer_recent;"
        ),
        
        # Course and enrollment performance indexes
        migrations.RunSQL(
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_enrollment_customer_recent ON crm_enrollment (customer_id, enrollment_date DESC) WHERE enrollment_date >= CURRENT_DATE - INTERVAL '1 year';",
            reverse_sql="DROP INDEX IF EXISTS idx_enrollment_customer_recent;"
        ),
        migrations.RunSQL(
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_course_active_start ON crm_course (start_date ASC, is_active) WHERE is_active = true AND start_date >= CURRENT_DATE;",
            reverse_sql="DROP INDEX IF EXISTS idx_course_active_start;"
        ),
        
        # YouTube message performance indexes
        migrations.RunSQL(
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_youtube_handle_status ON crm_youtubemessage (target_youtube_handle, status, sent_at DESC);",
            reverse_sql="DROP INDEX IF EXISTS idx_youtube_handle_status;"
        ),
        migrations.RunSQL(
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_youtube_pending ON crm_youtubemessage (created_at ASC) WHERE status = 'pending';",
            reverse_sql="DROP INDEX IF EXISTS idx_youtube_pending;"
        ),
        
        # Partial indexes for better performance on common queries
        migrations.RunSQL(
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_customer_corporate_clients ON crm_customer (company_primary, created_at DESC) WHERE customer_type = 'corporate' AND status = 'active';",
            reverse_sql="DROP INDEX IF EXISTS idx_customer_corporate_clients;"
        ),
        migrations.RunSQL(
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_customer_prospects_recent ON crm_customer (created_at DESC, source) WHERE status = 'prospect' AND created_at >= CURRENT_DATE - INTERVAL '6 months';",
            reverse_sql="DROP INDEX IF EXISTS idx_customer_prospects_recent;"
        ),
        
        # Covering indexes for frequent queries (PostgreSQL specific)
        migrations.RunSQL(
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_customer_list_covering ON crm_customer (status, created_at DESC) INCLUDE (first_name, last_name, email_primary, customer_type);",
            reverse_sql="DROP INDEX IF EXISTS idx_customer_list_covering;"
        ),
        migrations.RunSQL(
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_enrollment_stats_covering ON crm_enrollment (course_id, status) INCLUDE (customer_id, enrollment_date, payment_status);",
            reverse_sql="DROP INDEX IF EXISTS idx_enrollment_stats_covering;"
        ),
    ]