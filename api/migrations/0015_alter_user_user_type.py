# Generated by Django 5.0 on 2024-11-18 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_alter_registerotpverification_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('employee', 'Employee'), ('jobseeker', 'Jobseeker'), ('admin', 'Admin')], max_length=10),
        ),
    ]