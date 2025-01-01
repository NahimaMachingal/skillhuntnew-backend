from rest_framework import serializers
from .models import Subscription

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id', 'user', 'razorpay_order_id', 'razorpay_payment_id', 'razorpay_signature', 'status', 'created_at']

