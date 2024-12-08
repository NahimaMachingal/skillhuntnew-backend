# job/serializers.py
from rest_framework import serializers
from .models import Job, JobApplication

class JobSerializer(serializers.ModelSerializer):
    employer_user_id = serializers.IntegerField(source='employer.user.id', read_only=True)  # Add this line
    employer_username = serializers.CharField(source='employer.user.username', read_only=True)
    employer_company_name = serializers.CharField(source='employer.company_name', read_only=True)
    class Meta:
        model = Job
        fields = '__all__'


class JobApplicationSerializer(serializers.ModelSerializer):
    # Nested serialization for the job and applicant details
    employer_id = serializers.IntegerField(source='employer.id', read_only=True)  # Add this line
    job_title = serializers.CharField(source='job.title', read_only=True)
    employer_company_name = serializers.CharField(source='job.employer.company_name', read_only=True)
    employer_username = serializers.CharField(source='job.employer.user.username', read_only=True)  # New field
    applicant_email = serializers.EmailField(source='applicant.email', read_only=True)
    applicant_name = serializers.CharField(source='applicant.username', read_only=True)
    job_id = serializers.IntegerField(source='job.id', read_only=True)
    job_status = serializers.SerializerMethodField()
    is_active = serializers.SerializerMethodField()

    class Meta:
        model = JobApplication
        fields = '__all__'
        read_only_fields = ['applied_at']
    
    def get_job_status(self, obj):
        if not obj.job.is_active:
            return "Job is deleted by employer"
        return obj.job.status
    
    def get_is_active(self, obj):
        return obj.job.is_active