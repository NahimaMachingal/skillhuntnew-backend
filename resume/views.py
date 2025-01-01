#resume/views.py

from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import AboutMeSerializer, AddressSerializer, SkillSerializer, ProjectSerializer, EducationSerializer, ExperienceSerializer
from .models import AboutMe, Address, Skill, Project, Education, Experience
from rest_framework.response import Response
from rest_framework import status
from .permissions import IsEmployee, IsJobseeker, IsEmployeeOrJobseeker

class AboutMeView(APIView):
    permission_classes = [IsJobseeker]

    def get(self, request):
        about_me = AboutMe.objects.filter(user=request.user).order_by('-id').first()
        if not about_me:
            # Provide a default response
            return Response({
                "full_name": "",
                "position": "",
                "about": "",
                "profile_pic": None
            }, status=status.HTTP_200_OK)
        serializer = AboutMeSerializer(about_me)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request):
        # Make a mutable copy of the data
        data = request.data.copy()
        data['user'] = request.user.id  # Add the user field

        # Retrieve or create a new AboutMe instance for the user
        about_me = AboutMe.objects.filter(user=request.user).order_by('-id').first()
        if about_me:
            serializer = AboutMeSerializer(about_me, data=data, partial=True)
        else:
            serializer = AboutMeSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        print(serializer.errors)  
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AddressView(APIView):
    permission_classes = [IsJobseeker]

    def get(self, request):
        address = Address.objects.filter(user=request.user).order_by('-id').first()
        if not address:
            # Provide a default response
            return Response({
                "street": "",
                "city": "",
                "state": "",
                "country": "",
                "postal_code" : "",
                "phone": "",
            }, status=status.HTTP_200_OK)
        serializer = AddressSerializer(address)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # Make a mutable copy of the data
        data = request.data.copy()
        data['user'] = request.user.id  # Add the user field

        # Retrieve or create a new AboutMe instance for the user
        address = Address.objects.filter(user=request.user).order_by('-id').first()
        if address:
            serializer = AddressSerializer(address, data=data, partial=True)
        else:
            serializer = AddressSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class SkillView(CreateAPIView):
    permission_classes = [IsJobseeker]

    def get(self, request):
        skill = Skill.objects.filter(user=request.user).order_by('-id').first()
        if not skill:
            # Provide a default response
            return Response({
                "title": "",
                "soft_skills": "",
                "communication_skills": "",
                "other_skills": "",
                
            }, status=status.HTTP_200_OK)
        serializer = SkillSerializer(skill)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # Make a mutable copy of the data
        data = request.data.copy()
        data['user'] = request.user.id  # Add the user field

        # Retrieve or create a new AboutMe instance for the user
        skill = Skill.objects.filter(user=request.user).order_by('-id').first()
        if skill:
            serializer = SkillSerializer(skill, data=data, partial=True)
        else:
            serializer = SkillSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectsView(CreateAPIView):
    permission_classes = [IsJobseeker]
    def get(self, request):
        projects = Project.objects.filter(user=request.user).order_by('-id').first()
        if not projects:
            # Provide a default response
            return Response({
                "title": "",
                "description": "",
                "technologies_used": "",
                "start_date": "",
                "end_date" : "",
                
            }, status=status.HTTP_200_OK)
        serializer =    ProjectSerializer(projects)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # Make a mutable copy of the data
        data = request.data.copy()
        data['user'] = request.user.id  # Add the user field

        # Retrieve or create a new AboutMe instance for the user
        projects = Project.objects.filter(user=request.user).order_by('-id').first()
        if projects:
            serializer = ProjectSerializer(projects, data=data, partial=True)
        else:
            serializer = ProjectSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class EducationView(CreateAPIView):
    permission_classes = [IsJobseeker]
    def get(self, request):
        education = Education.objects.filter(user=request.user).order_by('-id').first()
        if not education:
            # Provide a default response
            return Response({
                "degree": "",
                "institution": "",
                "start_date": "",
                "end_date" : "",
                "grade" : "",
                
            }, status=status.HTTP_200_OK)
        serializer =    EducationSerializer(education)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # Make a mutable copy of the data
        data = request.data.copy()
        data['user'] = request.user.id  # Add the user field

        # Retrieve or create a new AboutMe instance for the user
        education = Education.objects.filter(user=request.user).order_by('-id').first()
        if education:
            serializer = EducationSerializer(education, data=data, partial=True)
        else:
            serializer = EducationSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ExperienceView(CreateAPIView):
    permission_classes = [IsJobseeker]
    def get(self, request):
        experience = Experience.objects.filter(user=request.user).order_by('-id').first()
        if not experience:
            # Provide a default response
            return Response({
                "job_title": "",
                "company_name": "",
                "start_date": "",
                "end_date" : "",
                "responsibilities" : "",
                
            }, status=status.HTTP_200_OK)
        serializer =    ExperienceSerializer(experience)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # Make a mutable copy of the data
        data = request.data.copy()
        data['user'] = request.user.id  # Add the user field

        # Retrieve or create a new AboutMe instance for the user
        experience = Experience.objects.filter(user=request.user).order_by('-id').first()
        if experience:
            serializer = ExperienceSerializer(experience, data=data, partial=True)
        else:
            serializer = ExperienceSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResumeDataView(APIView):
    permission_classes = [IsJobseeker]

    def get(self, request):
        user = request.user
        about_me = AboutMe.objects.get(user=user)
        address = Address.objects.get(user=user)
        skills = Skill.objects.filter(user=user)
        projects = Project.objects.filter(user=user)
        education = Education.objects.filter(user=user)
        experience = Experience.objects.filter(user=user)

        about_me_serializer = AboutMeSerializer(about_me)
        address_serializer = AddressSerializer(address)
        skills_serializer = SkillSerializer(skills, many=True)
        projects_serializer = ProjectSerializer(projects, many=True)
        education_serializer = EducationSerializer(education, many=True)
        experience_serializer = ExperienceSerializer(experience, many=True)

        data = {
            "aboutMe": about_me_serializer.data,
            "address": address_serializer.data,
            "skills": skills_serializer.data,
            "projects": projects_serializer.data,
            "education": education_serializer.data,
            "experience": experience_serializer.data,
        }

        return Response(data)