from django.urls import path
from .views import CreateSubscriptionView, VerifyPaymentView

urlpatterns = [
    path('create-subscription/', CreateSubscriptionView.as_view(), name='create-subscription'),
    path('verify-payment/', VerifyPaymentView.as_view(), name='verify-payment'),
]
