#api/urls.py

from django.urls import path, include
from . import views
from .views import *

from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

urlpatterns = [
    
    path('api/token/',TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('users/', get_users, name='get-users'),
    path('users/toggle-status/<int:user_id>/', toggle_user_status, name='toggle-user-status'),
    path('logout/', logout_view, name='logout'),
    path('profile/', JobseekerProfileView.as_view(), name='jobseeker-profile'),
    path('eprofile/', EmployerProfileView.as_view(), name='employer-profile'),
    
    
    path('google-login/', views.google_login, name='google-login'),  # New Google login endpoint


    path('send-otp/', SendOTPView.as_view(), name='send-otp'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),

    path('unverified-users/', UnverifiedUserListView.as_view(), name='unverified-users'),
    path('verify-user/<int:user_id>/', VerifyUserView.as_view(), name='verify-user'),

    
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('resend-otp/', ResendOTPView.as_view(), name='resend-otp'),


    #old

    path('user-list/',views.userList,name="user-list"),
    path('user-details/<int:pk>/',views.userDetails,name="user-details"),
    path('user-update/<int:pk>/',views.userUpdate,name="user-update"),
    path('user-delete/<int:pk>/',views.userDelete,name="user-delete"),
    path('class-userlist/',ClassUserList.as_view(),name='class-user-list'),

]

