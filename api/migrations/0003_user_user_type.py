# Generated by Django 5.0 on 2024-10-13 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_user_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('employee', 'Employee'), ('jobseeker', 'Jobseeker')], default='jobseeker', max_length=10),
        ),
    ]
