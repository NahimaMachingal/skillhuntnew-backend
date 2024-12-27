# interview/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Interview, Feedback
from django.contrib.auth.models import User
from chat.models import Notification
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=Interview)
def create_interview_notification(sender, instance, created, **kwargs):
    if created:
        # Attempt to find the applicant by their name or email
        applicant = None
        if instance.applicant:
            applicant = instance.applicant
        else:
            try:
                # If applicant is not directly available, attempt to retrieve by name or email
                applicant = User.objects.filter(email=instance.applicant_email).first()
                if not applicant:
                    print(f"Error: Could not find applicant with email {instance.applicant_email}")
                    return
            except AttributeError:
                print("Error: Applicant is missing and no email field is provided.")
                return
        
        # Construct notification message
        message = f"Interview scheduled for the Job {instance.job.title} on {instance.scheduled_date.strftime('%Y-%m-%d %H:%M')}."
        
        # Create the notification
        Notification.objects.create(
            user=applicant,  # Assuming job.employer is linked to User
            message=message,
            notification_type='APPLICATION_STATUS',
            is_read=False
        )


@receiver(post_save, sender=Feedback)
def create_feedback_notification(sender, instance, created, **kwargs):
    if created:
        interview = instance.interview
        applicant_email = interview.applicant_email
        if applicant_email:
            try:
                applicant = User.objects.get(email=applicant_email)
                Notification.objects.create(
                    user=applicant,  # The jobseeker
                    message=f"Feedback received for your interview for {interview.job.title}.",
                    notification_type='APPLICATION_STATUS',
                    is_read=False
                )
            except User.DoesNotExist:
                # Handle cases where the user does not exist
                pass