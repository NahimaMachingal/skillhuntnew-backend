from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import JobApplication
from chat.models import Notification

@receiver(post_save, sender=JobApplication)
def create_notification(sender, instance, created, **kwargs):
    # Check if the status was changed to Accepted or Rejected
    if not created and instance.status in ['Accepted', 'Rejected']:
        # Create a notification for the applicant
        message = f"Your application for '{instance.job.title}' has been {instance.status.lower()}."
        Notification.objects.create(
            user=instance.applicant,
            message=message,
            notification_type='APPLICATION_STATUS'
        )
