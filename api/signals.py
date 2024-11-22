# api/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import EmployerProfile, JobseekerProfile

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Check the user_type and create the respective profile
        if instance.user_type == 'employee':
            EmployerProfile.objects.get_or_create(user=instance)
        elif instance.user_type == 'jobseeker':
            JobseekerProfile.objects.get_or_create(user=instance)
