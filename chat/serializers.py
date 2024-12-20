#chat/serializers.py

from rest_framework import serializers
from .models import ChatRoom, Message, Notification
from django.contrib.auth import get_user_model
from api.models import JobseekerProfile, EmployerProfile


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username']

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'content', 'timestamp']

class ChatRoomSerializer(serializers.ModelSerializer):
    jobseeker = UserSerializer(read_only=True)
    employer = UserSerializer(read_only=True)
    jobseeker_profile_pic = serializers.SerializerMethodField()
    employer_profile_pic = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoom
        fields = ['id', 'jobseeker', 'employer', 'jobseeker_profile_pic', 'employer_profile_pic','created_at', 'last_message']

    def get_last_message(self, obj):
        last_message = obj.messages.order_by('-timestamp').first()
        if last_message:
            return MessageSerializer(last_message).data
        return None

    def get_jobseeker_profile_pic(self, obj):
        jobseeker_profile = JobseekerProfile.objects.filter(user=obj.jobseeker).first()
        if jobseeker_profile and jobseeker_profile.profile_img:
            return jobseeker_profile.profile_img.url
        return None
    
    def get_employer_profile_pic(self, obj):
        employer_profile = EmployerProfile.objects.filter(user=obj.employer).first()
        if employer_profile and employer_profile.profile_img:
            return employer_profile.profile_img.url
        return None
    
    

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'message', 'notification_type', 'is_read', 'created_at']