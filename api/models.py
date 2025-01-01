#api/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('employee', 'Employee'),
        ('jobseeker', 'Jobseeker'),
        ('admin', 'Admin'),
    )

    username=models.CharField(max_length= 250,unique=True)
    email=models.EmailField(max_length=250,unique=True)
    
    is_active=models.BooleanField(default=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)  # New Field
    is_verified = models.BooleanField(default=False)  # New Field
    is_subscribed = models.BooleanField(default=False)  # New Field

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username']

    def __str__(self):
        return self.email

class JobseekerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile')
    profile_img=models.ImageField(upload_to='profile',blank=True,null=True)
    phone_number = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    bio = models.TextField(blank=True)
    linkedin_url = models.URLField(blank=True)
    portfolio_url = models.URLField(blank=True)
    place = models.TextField(blank=True)
    current_job_title = models.CharField(max_length=100, blank=True)
    job_preferences = models.TextField(blank=True)
    visible_applications = models.JSONField(default=list, blank=True)
   
    def __str__(self):
        return f"{self.user.email} - Jobseeker Profile"

class EmployerProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    profile_img = models.ImageField(upload_to='profile',blank=True,null=True)
    phone_number = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    place = models.TextField(blank=True)
    company_name = models.CharField(max_length=250, blank=True)
    company_website = models.URLField(blank=True, null=True)  # Corrected field definition
    company_role = models.CharField(max_length=50, choices=[('admin', 'Admin'), ('manager', 'Manager')], default='admin')

    def __str__(self):
        # Display the employer's company name and role
        return f"{self.company_name} - {self.company_role}"



class OTPVerification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    creation_time = models.DateTimeField(default=timezone.now) 
    expiry_time = models.DateTimeField()

class RegisterOTPVerification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otp_verifications')
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return self.created_at >= timezone.now() - timedelta(minutes=10) 