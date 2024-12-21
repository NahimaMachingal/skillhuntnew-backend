#interview/models.py
from django.db import models
from api.models import User
from job.models import Job
from django.core.exceptions import ValidationError
import re


# Custom validator for the meeting_link field
def validate_custom_url(value):
    # Custom validation for URLs like https://82487-437
    if not re.match(r"^https://\d{5}-\d{3}$", value):  # Example pattern for https://XXXXX-XXX format
        raise ValidationError(f"{value} is not a valid meeting link.")

class Interview(models.Model):
    SCHEDULED = 'Scheduled'
    COMPLETED = 'Completed'
    CANCELLED = 'Cancelled'
    STATUS_CHOICES = [
        (SCHEDULED, 'Scheduled'),
        (COMPLETED, 'Completed'),
        (CANCELLED, 'Cancelled'),
    ]

    IN_PERSON = 'In-person'
    VIRTUAL = 'Virtual'
    MODE_CHOICES = [
        (IN_PERSON, 'In-person'),
        (VIRTUAL, 'Virtual'),
    ]
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interviews', null=True, blank=True)  # New field
    applicant_name = models.CharField(max_length=255, blank=True, null=True)  # Store name or email
    applicant_email = models.EmailField(blank=True, null=True)  # Optional, for identification
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='interviews')
    scheduled_date = models.DateTimeField()
    mode = models.CharField(max_length=20, choices=MODE_CHOICES)
    location = models.CharField(max_length=255, blank=True, null=True)  # For In-person
    meeting_link = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        validators=[validate_custom_url]  # Custom validator added here
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=SCHEDULED)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Interview for {self.applicant_name} - {self.job.title}"


class Feedback(models.Model):
    interview = models.OneToOneField(Interview, on_delete=models.CASCADE, related_name="feedback")
    interviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="given_feedback")
    rating = models.IntegerField(
        choices=[(i, i) for i in range(1, 6)],  # Ratings 1 to 5
        help_text="Rate from 1 (Poor) to 5 (Excellent)"
    )
    comments = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for {self.interview}"
