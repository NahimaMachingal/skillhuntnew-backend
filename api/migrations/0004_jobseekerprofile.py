# Generated by Django 5.1.2 on 2024-10-16 09:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_user_user_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobseekerProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(blank=True, max_length=15)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('bio', models.TextField(blank=True)),
                ('linkedin_url', models.URLField(blank=True)),
                ('portfolio_url', models.URLField(blank=True)),
                ('resume', models.FileField(blank=True, null=True, upload_to='jobseeker_resumes/')),
                ('current_job_title', models.CharField(blank=True, max_length=100)),
                ('job_preferences', models.TextField(blank=True)),
                ('visible_applications', models.JSONField(blank=True, default=list)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='employee_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
