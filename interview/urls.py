#interview/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('interview/schedule/', ScheduleInterviewView.as_view(), name='schedule-interview'),
path('interview/<int:pk>/', InterviewDetailView.as_view(), name='interview-detail'),
path('user-interviews/', UserInterviewListView.as_view(), name='user-interviews'),
path('employer-interviews/<int:job_id>/', EmployerJobInterviewsView.as_view(), name='employer-interviews'),
path('employer/interviews/', EmployerInterviewListView.as_view(), name='employer-interviews'),
path('interviewed-candidates/', InterviewedCandidatesView.as_view(), name='interviewed-candidates'),
path('feedback/', SubmitFeedbackView.as_view(), name='feedback'),
path('feedback/<int:interview_id>/', FeedbackReviewView.as_view(), name='feedback-review'),
path('jobseeker/feedbacks/', JobseekerFeedbackView.as_view(), name='jobseeker-feedbacks'),

]
