from rest_framework import serializers
from .models import AboutMe, Address, Skill, Project, Education, Experience
from api.models import User  # Your custom User model

# Serializer for AboutMe model
class AboutMeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AboutMe
        fields = ['user', 'full_name', 'position', 'about', 'profile_pic']


# Serializer for Address model
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['user', 'street', 'city', 'state', 'country', 'postal_code', 'phone']


# Serializer for Skill model
class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['user', 'title', 'soft_skills', 'communication_skills', 'other_skills']


# Serializer for Project model
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['user', 'title', 'description', 'technologies_used', 'start_date', 'end_date']


# Serializer for Education model
class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ['user', 'degree', 'institution', 'start_date', 'end_date', 'grade']


# Serializer for Experience model
class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = ['user', 'job_title', 'company_name', 'start_date', 'end_date', 'responsibilities']
