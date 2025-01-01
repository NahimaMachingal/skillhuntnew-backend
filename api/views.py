#api/views.py

from django.shortcuts import render
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth import login, logout
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.filters import SearchFilter, OrderingFilter
from .serializers import UserSerializer, JobseekerProfileSerializer, EmployerProfileSerializer
from .models import User, JobseekerProfile, EmployerProfile
from .permissions import IsEmployee, IsJobseeker, IsEmployeeOrJobseeker
import requests
from .models import RegisterOTPVerification

import random
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .models import User, OTPVerification  # Assume OTPVerification is an OTP model you need to add
from django.shortcuts import get_object_or_404



# API view for user registration

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        data = request.data
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if password != confirm_password:
            return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            user_type = serializer.validated_data.get('user_type', 'jobseeker')
            user = User.objects.create_user(
                email=serializer.validated_data['email'],
                username=serializer.validated_data['username'],
                first_name=serializer.validated_data['first_name'],
                password=password,
                last_name=serializer.validated_data['last_name'],
                user_type=user_type,
                is_verified=False  # Set is_verified to False for new users
            )

                         # Generate OTP
            otp = str(random.randint(100000, 999999))
            RegisterOTPVerification.objects.create(user=user, otp=otp)

            # Send OTP to email
            send_mail(
                'Verify your email',
                f'Your OTP is {otp}',
                'mh.nahima@gmail.com',  # Replace with your sender email
                [user.email],
            )


            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# api/views.py
class VerifyOTPView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')

        user = get_object_or_404(User, email=email)
        otp_record = RegisterOTPVerification.objects.filter(user=user).order_by('-created_at').first()

        if not otp_record or not otp_record.is_valid():
            return Response({'error': 'OTP expired or invalid'}, status=status.HTTP_400_BAD_REQUEST)

        if otp_record.otp == otp:
            user.is_active = True
            user.save()
            otp_record.delete()  # Clean up OTP record after successful verification
            return Response({'message': 'Email verified successfully'}, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

class ResendOTPView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        user = get_object_or_404(User, email=email)
        otp_record = RegisterOTPVerification.objects.filter(user=user).order_by('-created_at').first()

        # Cooldown check
        cooldown_period = timedelta(seconds=1)
        if otp_record and timezone.now() - otp_record.created_at < cooldown_period:
            remaining_time = (cooldown_period - (timezone.now() - otp_record.created_at)).seconds
            return Response(
                {"error": f"Please wait {remaining_time} seconds before requesting a new OTP."},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )
        
        

        # Generate a new OTP
        otp = str(random.randint(100000, 999999))
        RegisterOTPVerification.objects.create(user=user, otp=otp)

        # Send OTP
        send_mail(
            'Your OTP Code',
            f'Your new OTP is {otp}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
        )

        return Response({"message": "OTP sent successfully!"}, status=status.HTTP_200_OK)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = User.objects.filter(email=email).first()
        # Check if user exists
        if user is None:
            return Response(
                {'error': 'Incorrect username or password'},
                status=status.HTTP_401_UNAUTHORIZED
            )        
        # Check if the password is correct
        if not user.check_password(password):
            return Response(
                {'error': 'Incorrect username or password'},
                status=status.HTTP_401_UNAUTHORIZED            )
        
        # Check if the user is verified
        if not user.is_verified:
            return Response({'error': 'User not verified. Please contact admin.'}, status=status.HTTP_403_FORBIDDEN)
        # Create profile if not exists
        if user.user_type == 'employee' and not EmployerProfile.objects.filter(user=user).exists():
            EmployerProfile.objects.create(user=user)
        elif user.user_type == 'jobseeker' and not JobseekerProfile.objects.filter(user=user).exists():
            JobseekerProfile.objects.create(user=user)        
        refresh = RefreshToken.for_user(user)
        refresh['first_name'] = user.first_name
        content = {
            'email' : user.email,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_type': user.user_type,
        }

        return Response(content, status=status.HTTP_200_OK)


class UnverifiedUserListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        unverified_users = User.objects.filter(is_verified=False)
        serializer = UserSerializer(unverified_users, many=True)
        return Response(serializer.data)

class VerifyUserView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, user_id):
        user = User.objects.filter(id=user_id, is_verified=False).first()
        if user:
            user.is_verified = True
            user.save()
            return Response({'message': 'User verified successfully'}, status=status.HTTP_200_OK)
        return Response({'error': 'User not found or already verified'}, status=status.HTTP_404_NOT_FOUND)




@api_view(['GET'])
def get_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def toggle_user_status(request, user_id):
    try:
        user = User.objects.get(id=user_id)

        
        
        user.is_active = not user.is_active  # Toggle the is_active field
        user.save()
        return Response({'message': f"User {'blocked' if not user.is_active else 'unblocked'} successfully."}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsEmployeeOrJobseeker])
def logout_view(request):
    logout(request)
    return Response({'message': 'Logged out successfully'}, status=200)


class JobseekerProfileView(APIView):
    permission_classes = [IsEmployeeOrJobseeker]
    parser_classes = [MultiPartParser, FormParser]  # Enable parsing of form data and file uploads
    def get(self, request):
        try:
            # Fetch the jobseeker's profile using the current authenticated user
            profile = JobseekerProfile.objects.get(user=request.user)
            serializer = JobseekerProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except JobseekerProfile.DoesNotExist:
            # If no profile exists, return default values as undefined
            empty_data = {
                'user': {
                    'id': request.user.id,
                    'email': request.user.email,
                    'username': request.user.username,
                    'first_name': request.user.first_name,
                    'last_name': request.user.last_name,
                    'is_active': request.user.is_active,
                    'user_type': request.user.user_type,
                },
                'profile_img': None,
                'phone_number': None,
                'date_of_birth': None,
                'bio': '',
                'linkedin_url': '',
                'portfolio_url': '',
                 'place': '',
                'current_job_title': '',
                'job_preferences': '',
                'visible_applications': [],
            }
            return Response(empty_data, status=status.HTTP_200_OK)
    
    def put(self, request):
        try:
            profile = JobseekerProfile.objects.get(user=request.user)
            serializer = JobseekerProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JobseekerProfile.DoesNotExist:
            # If the profile does not exist, create a new one
            serializer = JobseekerProfileSerializer(data=request.data, partial=True)
            if serializer.is_valid():
                # Set the user field to the current authenticated user
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            # Log or print error details for debugging
            print("Validation errors while creating profile:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Catch any other unexpected exceptions
            print("An error occurred:", str(e))
            return Response({"detail": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class EmployerProfileView(APIView):
    permission_classes = [IsEmployeeOrJobseeker]
    parser_classes = [MultiPartParser, FormParser]  # Enable parsing of form data and file uploads
    def get(self, request):
        try:
            # Fetch the employer's profile using the current authenticated user
            profile = EmployerProfile.objects.get(user=request.user)
            serializer = EmployerProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except EmployerProfile.DoesNotExist:
            # If no profile exists, return default values as undefined
            empty_data = {
                'user': {
                    'id': request.user.id,
                    'email': request.user.email,
                    'username': request.user.username,
                    'first_name': request.user.first_name,
                    'last_name': request.user.last_name,
                    'is_active': request.user.is_active,
                    'user_type': request.user.user_type,
                },
                'profile_img': None,
                'phone_number': None,
                'date_of_birth': None,
                'place': '',
                'company_name': '',
                'company_website': '',
                'company_role': '',
            }
            return Response(empty_data, status=status.HTTP_200_OK)
    
    def put(self, request):
        try:
            profile = EmployerProfile.objects.get(user=request.user)
            serializer = EmployerProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except EmployerProfile.DoesNotExist:
            # If the profile does not exist, create a new one
            serializer = EmployerProfileSerializer(data=request.data, partial=True)
            if serializer.is_valid():
                # Set the user field to the current authenticated user
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            # Log or print error details for debugging
            print("Validation errors while creating profile:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Catch any other unexpected exceptions
            print("An error occurred:", str(e))
            return Response({"detail": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def google_login(request):
    token = request.data.get('token')
    if not token:
        return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)

    # Verify the token
    response = requests.get(f'https://oauth2.googleapis.com/tokeninfo?id_token={token}')
    
    if response.status_code != 200:
        return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

    user_info = response.json()
    email = user_info.get('email')
    

  # Check if the user exists
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        # User not registered
        return Response({'error': 'User not registered'}, status=status.HTTP_403_FORBIDDEN)

    # Generate tokens
    refresh = RefreshToken.for_user(user)
    content = {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user_type': user.user_type,
    }

    return Response(content, status=status.HTTP_200_OK)







# Generate OTP and send email
class SendOTPView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()
        
        if not user:
            return Response({"error": "User with this email does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        # Check cooldown period before resending OTP
        cooldown_period = timedelta(seconds=1)  # Allow resending OTP every 30 seconds
        recent_otp = OTPVerification.objects.filter(user=user).order_by('-creation_time').first()
        
        if recent_otp and timezone.now() - recent_otp.creation_time < cooldown_period:
            remaining_time = (cooldown_period - (timezone.now() - recent_otp.creation_time)).seconds
            return Response(
                {"error": f"Please wait {remaining_time} seconds before requesting a new OTP."},
                status=status.HTTP_429_TOO_MANY_REQUESTS
    )

        # Generate OTP
        otp = random.randint(100000, 999999)
        expiry_time = timezone.now() + timedelta(minutes=5)  # OTP expires in 5 minutes

        # Store OTP in the OTPVerification model
        OTPVerification.objects.create(user=user, otp=otp, expiry_time=expiry_time)

        # Send OTP to the user's email
        send_mail(
            'Password Reset OTP',
            f'Your OTP for password reset is: {otp}',
            settings.DEFAULT_FROM_EMAIL,
            [email]
        )

        return Response({"message": "OTP sent successfully"}, status=status.HTTP_200_OK)


# Verify OTP and reset password
class ResetPasswordView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        new_password = request.data.get('new_password')

        user = get_object_or_404(User, email=email)
        otp_verification = OTPVerification.objects.filter(user=user, otp=otp, expiry_time__gte=timezone.now()).first()

        if not otp_verification:
            return Response({"error": "Invalid or expired OTP"}, status=status.HTTP_400_BAD_REQUEST)

        # Update password
        user.set_password(new_password)
        user.save()
        
        # Clean up used OTP
        otp_verification.delete()

        return Response({"message": "Password reset successful"}, status=status.HTTP_200_OK)













#old    

# API view to list all non-superuser users
@api_view(['GET'])
def userList(request):
    keyword = request.GET.get('search', None)
    # Query the database to get all users who are not superusers
    users = User.objects.filter(is_superuser=False)
    
    # Serialize the user data
    serializer = UserSerializer(users, many=True)
    
    # Set up filters for search and ordering (although not applied in this view)
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['id']  # Specify which fields are searchable
    
    # Return the serialized user data as a response
    return Response(serializer.data)

# API view to get details of a single user by primary key
@api_view(['GET'])
def userDetails(request, pk):
    try:
        # Try to retrieve the user with the given primary key
        user = User.objects.get(id=pk)
        
        # Serialize the user data
        serializer = UserSerializer(user, many=False)
        
        # Return the serialized user data as a response
        return Response(serializer.data)
    except User.DoesNotExist:
        # Return a 404 response if the user does not exist
        return Response("User not found!", status=status.HTTP_404_NOT_FOUND)

# API view to update user details by primary key
@api_view(['PUT', 'PATCH'])
def userUpdate(request, pk):
    try:
        # Retrieve the user with the given primary key
        user = User.objects.get(id=pk)
        
        # Instantiate the UserSerializer with the existing user and the updated data
        serializer = UserSerializer(user, data=request.data, partial=True)
        
        # Validate the updated data
        if serializer.is_valid():
            # Save the updated user data to the database
            serializer.save()
            
            # Return the serialized updated user data as a response
            return Response(serializer.data)
        else:
            # Return validation errors if any
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        # Return a 404 response if the user does not exist
        return Response("User not found!", status=status.HTTP_404_NOT_FOUND)

# API view to delete a user by primary key
@api_view(['DELETE'])
def userDelete(request, pk):
    try:
        # Try to retrieve the user with the given primary key, excluding the superuser with id 1
        user = User.objects.exclude(id=1).get(id=pk)
        
        # Delete the user from the database
        user.delete()
        
        # Return a success message
        return Response('User deleted')
    except User.DoesNotExist:
        # Return a 404 response if the user does not exist
        return Response("User not found")

# Generic view for listing and creating users
class ClassUserList(ListCreateAPIView):
    # Queryset to filter out superusers from the list
    queryset = User.objects.filter(is_superuser=False)
    
    # Serializer class to use for the queryset
    serializer_class = UserSerializer
    
    # Filter backends to apply search functionality
    filter_backends = [SearchFilter]
    
    # Fields that are searchable
    search_fields = ['username', 'email']