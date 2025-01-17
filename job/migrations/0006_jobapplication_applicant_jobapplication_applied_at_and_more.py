# Generated by Django 5.0 on 2024-10-26 08:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_employerprofile_delete_employer'),
        ('job', '0005_remove_jobapplication_applicant_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobapplication',
            name='applicant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='api.jobseekerprofile'),
        ),
        migrations.AddField(
            model_name='jobapplication',
            name='applied_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='jobapplication',
            name='cover_letter',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='jobapplication',
            name='job',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='job.job'),
        ),
        migrations.AddField(
            model_name='jobapplication',
            name='resume',
            field=models.FileField(null=True, upload_to='resumes/'),
        ),
        migrations.AddField(
            model_name='jobapplication',
            name='status',
            field=models.CharField(default='pending', max_length=20),
        ),
    ]
