import razorpay
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .models import Subscription
from .serializers import SubscriptionSerializer
from .permissions import IsEmployee, IsJobseeker, IsEmployeeOrJobseeker

# Initialize Razorpay client
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

class CreateSubscriptionView(APIView):
    permission_classes = [IsJobseeker]

    def post(self, request):
        user = request.user
        amount = 2999  # Amount in paise (₹29.99)
        currency = 'INR'

        # Create Razorpay order
        try:
            razorpay_order = razorpay_client.order.create({
                "amount": amount,
                "currency": currency,
                "payment_capture": "1"
            })

            subscription = Subscription.objects.create(
                user=user,
                razorpay_order_id=razorpay_order['id'],
                status="PENDING"
            )

            return Response({
                "order_id": razorpay_order['id'],
                "amount": amount,
                "currency": currency
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class VerifyPaymentView(APIView):
    permission_classes = [IsJobseeker]

    def post(self, request):
        data = request.data
        try:
            # Verify payment signature
            razorpay_client.utility.verify_payment_signature(data)

            subscription = Subscription.objects.get(razorpay_order_id=data['razorpay_order_id'])

             # Log to debug and check if the subscription is being fetched
            print(f"Subscription found: {subscription}")


            # Check if the payment_id and signature are present in the request
            if 'razorpay_payment_id' not in data or 'razorpay_signature' not in data:
                return Response({"error": "Payment ID or signature missing."}, status=status.HTTP_400_BAD_REQUEST)


            subscription.razorpay_payment_id = data['razorpay_payment_id']
            subscription.razorpay_signature = data['razorpay_signature']
            subscription.status = "COMPLETED"
            subscription.save()

            # Log to check if the subscription was saved properly
            print(f"Updated subscription: {subscription}")

            return Response({"message": "Payment verified successfully."}, status=status.HTTP_200_OK)
        except razorpay.errors.SignatureVerificationError:
            return Response({"error": "Invalid signature."}, status=status.HTTP_400_BAD_REQUEST)
        except Subscription.DoesNotExist:
            return Response({"error": "Subscription not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
