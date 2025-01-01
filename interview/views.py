from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import InterviewSerializer, EmployerInterviewSerializer, FeedbackSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Interview, Feedback
from job.models import Job
from rest_framework import status
from .permissions import IsEmployee, IsJobseeker, IsEmployeeOrJobseeker

class ScheduleInterviewView(CreateAPIView):
    permission_classes = [IsEmployeeOrJobseeker]
    serializer_class = InterviewSerializer

class InterviewDetailView(RetrieveAPIView):
    permission_classes = [IsEmployeeOrJobseeker]

    def get(self, request, pk):
        interview = Interview.objects.get(pk=pk)
        serializer = InterviewSerializer(interview)
        return Response(serializer.data)

    def patch(self, request, pk):
        interview = Interview.objects.get(pk=pk)
        data = request.data
        interview.status = data.get('status', interview.status)
        interview.save()
        serializer = InterviewSerializer(interview)
        return Response(serializer.data, status=status.HTTP_200_OK)

        
class UserInterviewListView(APIView):
    permission_classes = [IsEmployeeOrJobseeker]

    def get(self, request):
        # Filter interviews by the authenticated user's email
        interviews = Interview.objects.filter(applicant_email=request.user.email)
        serializer = InterviewSerializer(interviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class EmployerJobInterviewsView(APIView):
    permission_classes = [IsEmployeeOrJobseeker]

    def get(self, request, job_id):
        # Fetch interviews for the given job_id
        interviews = Interview.objects.filter(job__id=job_id)
        serializer = EmployerInterviewSerializer(interviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EmployerInterviewListView(APIView):
    permission_classes = [IsEmployeeOrJobseeker]

    def get(self, request):
        # Get the employer's jobs by filtering Job objects related to the authenticated employer
        employer_jobs = Job.objects.filter(employer=request.user.employerprofile)
        # Filter interviews based on the jobs associated with the employer
        interviews = Interview.objects.filter(job__in=employer_jobs)
        
        serializer = InterviewSerializer(interviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class InterviewedCandidatesView(APIView):
    permission_classes = [IsEmployeeOrJobseeker]

    def get(self, request):
        interviewed_candidates = Interview.objects.filter(status="Completed")
        serializer = InterviewSerializer(interviewed_candidates, many=True)
        return Response(serializer.data)

import logging

logger = logging.getLogger(__name__)

class SubmitFeedbackView(APIView):
    permission_classes = [IsEmployeeOrJobseeker]

    def post(self, request):
        logger.info(f"Received feedback data: {request.data}")
        try:
            interview_id = request.data.get('interviewId')
            interview = Interview.objects.get(id=interview_id)
            feedback_data = {
                'interview': interview.id,
                'interviewer': request.user.id,
                'rating': request.data.get('rating'),
                'comments': request.data.get('comments'),
            }
            serializer = FeedbackSerializer(data=feedback_data)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Feedback saved: {serializer.data}")
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            logger.error(f"Validation errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Interview.DoesNotExist:
            logger.error(f"Interview with id {interview_id} not found")
            return Response({"error": "Interview not found"}, status=status.HTTP_404_NOT_FOUND)



class FeedbackReviewView(APIView):
    permission_classes = [IsEmployeeOrJobseeker]

    def get(self, request, interview_id):
        try:
            interview = Interview.objects.get(id=interview_id)
            feedback = Feedback.objects.get(interview=interview)
            serializer = FeedbackSerializer(feedback)
            return Response(serializer.data)
        except Interview.DoesNotExist:
            return Response({"detail": "Interview not found."}, status=status.HTTP_404_NOT_FOUND)
        except Feedback.DoesNotExist:
            return Response({"detail": "Feedback not found."}, status=status.HTTP_404_NOT_FOUND)

    
class JobseekerFeedbackView(APIView):
    permission_classes = [IsEmployeeOrJobseeker]

    def get(self, request):
        # Fetch the logged-in user's email
        jobseeker_email = request.user.email
        
        # Fetch interviews where the applicant_email matches the jobseeker's email
        interviews = Interview.objects.filter(applicant_email=jobseeker_email)
        
        # Filter feedbacks by these interviews
        feedbacks = Feedback.objects.filter(interview__in=interviews)
        
        # Serialize the feedbacks
        serializer = FeedbackSerializer(feedbacks, many=True)
        return Response(serializer.data)