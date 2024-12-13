from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import InterviewSerializer, EmployerInterviewSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Interview
from rest_framework import status

class ScheduleInterviewView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InterviewSerializer

class InterviewDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Interview.objects.all()
    serializer_class = InterviewSerializer

class UserInterviewListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Filter interviews by the authenticated user's email
        interviews = Interview.objects.filter(applicant_email=request.user.email)
        serializer = InterviewSerializer(interviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class EmployerJobInterviewsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, job_id):
        # Fetch interviews for the given job_id
        interviews = Interview.objects.filter(job__id=job_id)
        serializer = EmployerInterviewSerializer(interviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)