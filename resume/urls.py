#resume/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    
    path('about-me/', AboutMeView.as_view(), name='about-me'),
   
    path('address/', AddressView.as_view(), name='address'),
    path('skills/', SkillView.as_view(), name='create-skill'),
    path('projects/', ProjectsView.as_view(), name='create-projects'),
    path('education/', EducationView.as_view(), name='create-education'),
    path('experience/', ExperienceView.as_view(), name='create-experience'),
    path('resume/', ResumeDataView.as_view(), name='get-resume-data'),

]