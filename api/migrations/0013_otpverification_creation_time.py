# Generated by Django 5.0 on 2024-11-17 16:17

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_registerotpverification'),
    ]

    operations = [
        migrations.AddField(
            model_name='otpverification',
            name='creation_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
