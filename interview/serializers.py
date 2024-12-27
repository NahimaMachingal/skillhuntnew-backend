#interview/serializers.py

from rest_framework import serializers
from .models import Interview, Feedback


class InterviewSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source='job.title', read_only=True)
    has_feedback = serializers.SerializerMethodField()
   

    class Meta:
        model = Interview
        fields = '__all__'
        
    def get_has_feedback(self, obj):
        return Feedback.objects.filter(interview=obj).exists()

class EmployerInterviewSerializer(serializers.ModelSerializer):
    applicant_name = serializers.CharField()
    applicant_email = serializers.EmailField()
    job_title = serializers.CharField(source='job.title', read_only=True)

    class Meta:
        model = Interview
        fields = '__all__'
        


class FeedbackSerializer(serializers.ModelSerializer):
    # Nested representation for interviewer details if needed
    interviewer_email = serializers.EmailField(source='interviewer.email', read_only=True)
    job_title = serializers.CharField(source='interview.job.title', read_only=True)  # Add this
    interviewer_name = serializers.CharField(source='interviewer.username', read_only=True)  # Add this

    class Meta:
        model = Feedback
        fields = [
            'id', 'interview', 'interviewer', 'interviewer_email', 'job_title', 'interviewer_name' ,'rating', 
            'comments', 'created_at'
        ]
        read_only_fields = ['created_at']
