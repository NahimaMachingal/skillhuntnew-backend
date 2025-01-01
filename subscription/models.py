from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from api.models import User

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Subscription for {self.user.email} - {self.status}"


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update the is_subscribed field of the user
        if self.status.upper() == "COMPLETED":
            self.user.is_subscribed = True
        else:
            self.user.is_subscribed = False
        self.user.save()