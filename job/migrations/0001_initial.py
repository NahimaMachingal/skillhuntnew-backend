# Generated by Django 5.0 on 2024-10-20 19:14

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('api', '0009_employerprofile_delete_employer'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='JobSkill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('responsibilities', models.TextField(blank=True, null=True)),
                ('qualifications', models.TextField(blank=True, null=True)),
                ('nice_to_have', models.TextField(blank=True, null=True)),
                ('employment_type', models.CharField(choices=[('Full-time', 'Full-time'), ('Part-time', 'Part-time'), ('Contract', 'Contract'), ('Temporary', 'Temporary'), ('Internship', 'Internship'), ('Freelance', 'Freelance')], max_length=50)),
                ('location', models.CharField(blank=True, max_length=100, null=True)),
                ('salary_min', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('salary_max', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('is_remote', models.BooleanField(default=False)),
                ('application_deadline', models.DateField(blank=True, null=True)),
                ('posted_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.CharField(default='open', max_length=20)),
                ('views_count', models.IntegerField(default=0)),
                ('applications_count', models.IntegerField(default=0)),
                ('experience_level', models.CharField(blank=True, choices=[('Entry level', 'Entry level'), ('Mid level', 'Mid level'), ('Senior level', 'Senior level'), ('Executive', 'Executive')], max_length=50, null=True)),
                ('job_function', models.CharField(blank=True, max_length=100, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('employer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to='api.employerprofile')),
                ('skills_required', models.ManyToManyField(blank=True, related_name='jobs', to='job.jobskill')),
            ],
        ),
    ]