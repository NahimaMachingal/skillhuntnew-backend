# Generated by Django 5.1.2 on 2024-12-30 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subscription',
            old_name='start_date',
            new_name='created_at',
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='active',
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='stripe_customer_id',
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='stripe_subscription_id',
        ),
        migrations.AddField(
            model_name='subscription',
            name='razorpay_order_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='subscription',
            name='razorpay_payment_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='subscription',
            name='razorpay_signature',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='subscription',
            name='status',
            field=models.CharField(default='PENDING', max_length=20),
        ),
    ]
