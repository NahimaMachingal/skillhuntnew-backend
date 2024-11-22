from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework.decorators import api_view
from .models import JobseekerProfile
from .serializers import JobseekerProfileSerializer
from api.permissions import IsJobseeker
from rest_framework.decorators import api_view, permission_classes
# Add this import at the top of your views.py file
from rest_framework.generics import RetrieveAPIView

from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.views import APIView

class JobseekerProfileView(RetrieveAPIView):
    serializer_class = JobseekerProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        return JobseekerProfile.objects.get(user=user)