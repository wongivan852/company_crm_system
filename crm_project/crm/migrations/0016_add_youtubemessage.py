# Generated manually on 2025-08-01 02:58

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("crm", "0015_make_names_optional_for_youtubers"),
    ]

    operations = [
        migrations.CreateModel(
            name="YouTubeMessage",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "message_type",
                    models.CharField(
                        choices=[
                            ("direct_message", "Direct Message"),
                            ("comment", "Video Comment"),
                            ("community_post", "Community Post"),
                            ("collaboration", "Collaboration Request"),
                            ("business", "Business Inquiry"),
                        ],
                        default="direct_message",
                        max_length=20,
                    ),
                ),
                (
                    "subject",
                    models.CharField(
                        help_text="Message subject or title", max_length=200
                    ),
                ),
                ("content", models.TextField(help_text="Message content")),
                (
                    "target_youtube_handle",
                    models.CharField(
                        help_text="YouTube handle to send to", max_length=100
                    ),
                ),
                (
                    "target_video_url",
                    models.URLField(
                        blank=True, help_text="Specific video URL if commenting"
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("draft", "Draft"),
                            ("pending", "Pending Send"),
                            ("sent", "Sent"),
                            ("delivered", "Delivered"),
                            ("read", "Read"),
                            ("replied", "Replied"),
                            ("failed", "Failed"),
                            ("bounced", "Bounced"),
                        ],
                        default="draft",
                        max_length=20,
                    ),
                ),
                (
                    "priority",
                    models.IntegerField(default=3, help_text="1=High, 2=Medium, 3=Low"),
                ),
                (
                    "sent_by",
                    models.CharField(
                        blank=True, help_text="Who sent the message", max_length=100
                    ),
                ),
                ("sent_at", models.DateTimeField(blank=True, null=True)),
                ("response_received", models.BooleanField(default=False)),
                (
                    "response_content",
                    models.TextField(
                        blank=True, help_text="Response received from YouTuber"
                    ),
                ),
                ("response_received_at", models.DateTimeField(blank=True, null=True)),
                ("message_opened", models.BooleanField(default=False)),
                ("opened_at", models.DateTimeField(blank=True, null=True)),
                ("click_count", models.IntegerField(default=0)),
                (
                    "error_message",
                    models.TextField(
                        blank=True, help_text="Error details if send failed"
                    ),
                ),
                ("retry_count", models.IntegerField(default=0)),
                ("max_retries", models.IntegerField(default=3)),
                (
                    "external_message_id",
                    models.CharField(
                        blank=True,
                        help_text="External service message ID",
                        max_length=200,
                    ),
                ),
                (
                    "platform_data",
                    models.JSONField(
                        blank=True, default=dict, help_text="Platform-specific data"
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="youtube_messages",
                        to="crm.customer",
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
        migrations.AddIndex(
            model_name="youtubemessage",
            index=models.Index(
                fields=["customer", "status"], name="crm_youtube_custome_ecde93_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="youtubemessage",
            index=models.Index(
                fields=["target_youtube_handle"], name="crm_youtube_target__d217b5_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="youtubemessage",
            index=models.Index(
                fields=["sent_at"], name="crm_youtube_sent_at_b120b4_idx"
            ),
        ),
    ]