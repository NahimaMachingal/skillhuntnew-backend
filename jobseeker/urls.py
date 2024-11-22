from django.urls import path
from .import views
from .views import JobseekerProfileView

urlpatterns = [
    
    path('jobseeker/profile/', JobseekerProfileView.as_view(), name='jobseeker-profile'),
]