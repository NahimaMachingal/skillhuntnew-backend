from django.contrib import admin
from .models import User,JobseekerProfile, EmployerProfile, OTPVerification, RegisterOTPVerification
# Register your models here.
admin.site.register(User)
admin.site.register(JobseekerProfile)
admin.site.register(EmployerProfile)
admin.site.register(OTPVerification)
admin.site.register(RegisterOTPVerification)