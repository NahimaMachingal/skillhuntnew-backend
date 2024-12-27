#job/models.py

from django.db import models
from api.models import EmployerProfile, JobseekerProfile, User
from django.utils import timezone


# Create your models here.


class Job(models.Model):
    FULL_TIME = 'Full-time'
    PART_TIME = 'Part-time'
    CONTRACT = 'Contract'
    TEMPORARY = 'Temporary'
    INTERNSHIP = 'Internship'
    FREELANCE = 'Freelance'
    EMPLOYMENT_TYPE_CHOICES = [
        (FULL_TIME, 'Full-time'),
        (PART_TIME, 'Part-time'),
        (CONTRACT, 'Contract'),
        (TEMPORARY, 'Temporary'),
        (INTERNSHIP, 'Internship'),
        (FREELANCE, 'Freelance'),
    ]

    # Choices for experience_level
    ENTRY_LEVEL = 'Entry level'
    MID_LEVEL = 'Mid level'
    SENIOR_LEVEL = 'Senior level'
    EXECUTIVE = 'Executive'
    EXPERIENCE_LEVEL_CHOICES = [
        (ENTRY_LEVEL, 'Entry level'),
        (MID_LEVEL, 'Mid level'),
        (SENIOR_LEVEL, 'Senior level'),
        (EXECUTIVE, 'Executive'),
    ]
    employer = models.ForeignKey(EmployerProfile, related_name='jobs', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    responsibilities = models.TextField(blank=True, null=True)
    qualifications = models.TextField(blank=True, null=True)
    nice_to_have = models.TextField(blank=True, null=True)
    employment_type = models.CharField(max_length=50, choices=EMPLOYMENT_TYPE_CHOICES)
    location = models.CharField(max_length=100, blank=True, null=True)
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    is_remote = models.BooleanField(default=False)
    application_deadline = models.DateField(blank=True, null=True)
    posted_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, default='open')
    experience_level = models.CharField(max_length=50, choices=EXPERIENCE_LEVEL_CHOICES, blank=True, null=True)
    job_function = models.CharField(max_length=100, blank=True, null=True)
    is_approved = models.BooleanField(default=False)  # New field added
    currency = models.CharField(max_length=10, default='AED')
    is_active = models.BooleanField(default=True) 

    def __str__(self):
        return self.title

class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Reviewed', 'Reviewed'),
        ('Interview', 'Interview'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]

    
    job = models.ForeignKey(Job, on_delete=models.CASCADE, null=True)
    applicant = models.ForeignKey(User, related_name='job_applications', on_delete=models.CASCADE, null=True)
    resume = models.FileField(upload_to='resumes/', null=True)
    cover_letter = models.TextField(blank=True, null=True)
    applied_at = models.DateTimeField(auto_now_add=True, null = True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')  # Example status field
    questions = models.JSONField(blank=True, null=True)  # Updated JSONField import
    reason = models.TextField(blank=True, null=True)


    def __str__(self):
        job_title = self.job.title if self.job else 'No job assigned'
        return f"{self.applicant.email} applied for {job_title}"
