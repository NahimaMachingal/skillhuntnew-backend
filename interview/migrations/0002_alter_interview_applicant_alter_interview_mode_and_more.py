# Generated by Django 5.1.2 on 2024-12-10 04:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interview', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='interview',
            name='applicant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='interviews', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='interview',
            name='mode',
            field=models.CharField(choices=[('In-person', 'In-person'), ('Virtual', 'Virtual')], max_length=20),
        ),
        migrations.AlterField(
            model_name='interview',
            name='status',
            field=models.CharField(choices=[('Scheduled', 'Scheduled'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], default='Scheduled', max_length=20),
        ),
    ]