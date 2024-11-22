# job/serializers.py
from rest_framework import serializers
from .models import Job, JobApplication

class JobSerializer(serializers.ModelSerializer):
    employer_username = serializers.CharField(source='employer.user.username', read_only=True)
    employer_company_name = serializers.CharField(source='employer.company_name', read_only=True)
    class Meta:
        model = Job
        fields = '__all__'


class JobApplicationSerializer(serializers.ModelSerializer):
    # Nested serialization for the job and applicant details
    job_title = serializers.CharField(source='job.title', read_only=True)
    employer_company_name = serializers.CharField(source='job.employer.company_name', read_only=True)
    employer_username = serializers.CharField(source='job.employer.user.username', read_only=True)  # New field
    applicant_email = serializers.EmailField(source='applicant.email', read_only=True)
    applicant_name = serializers.CharField(source='applicant.username', read_only=True)
    
    class Meta:
        model = JobApplication
        fields = [
            'id',
            'job',
            'job_title',
            'employer_company_name',
            'employer_username',
            'applicant',
            'applicant_email',
            'applicant_name',
            'resume',
            'cover_letter',
            'applied_at',
            'status',
            'questions',
        ]
        read_only_fields = ['applied_at']