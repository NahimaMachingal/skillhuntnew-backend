#api/urls.py

from django.urls import path
from . import views
from .views import *


urlpatterns = [
    
    path('post/', PostJobView.as_view(), name='post-job'),
    path('jobs/', JobListView.as_view(), name='job-list'),
    path('pending-jobs/', PendingJobListView.as_view(), name='pending-jobs'),  # Add this line
    path('job/<int:id>/', JobDetailView.as_view(), name='job-detail'),  # Add this line for JobDetail
    path('job/jobseeker/<int:id>/', JobSeekerJobDetailView.as_view(), name='jobseeker-job-detail'),  # New URL for jobseeker
    path('job/approve/<int:id>/', ApproveJobView.as_view(), name='approve-job'),
    path('approved-jobs/', ApprovedJobListView.as_view(), name='approved-jobs'),
    path('apply/', JobApplicationCreateView.as_view(), name='job-application-create'),
    path('admin/jobs/', AdminJobListView.as_view(), name='admin-job-list'),  # List all jobs for admin
    path('applied-candidates/', AppliedCandidatesView.as_view(), name='applied-candidates'),
    path('application/<int:application_id>/', UpdateApplicationStatusView.as_view(), name='update-application-status'),
    path('admin/applications/', AdminJobApplicationsView.as_view(), name='admin-applications'),
    path('updatejob/<int:job_id>/', UpdateJobView.as_view(), name='update-job'),
    path('job/<int:job_id>/applicants/', ApplicantsForJobView.as_view(), name='applicants-for-job'),
    path('user/applied-jobs/', UserAppliedJobsView.as_view(), name='user-applied-jobs'),
    path('jobs/<int:job_id>/is-applied/', CheckJobApplicationView.as_view(), name='check-job-application'),
    path('application/<int:application_id>/reason/', UpdateReasonView.as_view(), name='update-reason'),
    path('user/rejected-jobs/', RejectedJobsView.as_view(), name='rejected-jobs'),

]