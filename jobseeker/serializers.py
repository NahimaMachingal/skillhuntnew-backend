# jobseeker/serializers.py
from rest_framework import serializers
from api.serializers import UserSerializer,JobseekerProfile
from .models import Education, WorkExperience, Skill

class JobseekerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Nested serializer for User

    class Meta:
        model = JobseekerProfile
        fields = [
            'user', 'phone_number', 'date_of_birth', 'bio',
            'linkedin_url', 'portfolio_url', 'resume',
            'current_job_title', 'job_preferences', 'visible_applications'
        ]

    def create(self, validated_data):
        # Extract user data from validated data
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)

        # Create JobseekerProfile instance
        jobseeker_profile = JobseekerProfile.objects.create(user=user, **validated_data)
        return jobseeker_profile

    def update(self, instance, validated_data):
        # Update user information
        user_data = validated_data.pop('user')
        user = instance.user
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()

        # Update JobseekerProfile instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = [
            'id', 'job_seeker', 'degree_type', 'field_of_study', 
            'institution', 'location', 'start_date', 'end_date', 
            'grade_or_gpa', 'description'
        ]

class WorkExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperience
        fields = [
            'id', 'job_seeker', 'job_title', 'company_name', 
            'company_location', 'start_date', 'end_date', 
            'technologies_used'
        ]

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = [
            'id', 'job_seeker', 'skill_name', 'proficiency_level', 
            'years_of_experience', 'certification', 'skill_type'
        ]
