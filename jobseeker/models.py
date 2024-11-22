#jobseeker/models.py
from django.db import models
from api.models import JobseekerProfile
# Create your models here.


class Education(models.Model):
    
    job_seeker = models.ForeignKey(JobseekerProfile, related_name='educations', on_delete=models.CASCADE)
    degree_type = models.CharField(max_length=50, choices=[('Diploma', 'Diploma'), ('Bachelor', 'Bachelor'), ('Master', 'Master'), ('PhD', 'PhD'), ('Certification', 'Certification')])
    field_of_study = models.CharField(max_length=100)
    institution = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    grade_or_gpa = models.CharField(max_length=20, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

class WorkExperience(models.Model):
    job_seeker = models.ForeignKey(JobseekerProfile, related_name='work_experience', on_delete=models.CASCADE)
    job_title = models.CharField(max_length=100)
    company_name = models.CharField(max_length=200)
    company_location = models.CharField(max_length=100, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    technologies_used = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.job_title} at {self.company_name}"

class Skill(models.Model):
    job_seeker = models.ForeignKey(JobseekerProfile, related_name='skills', on_delete=models.CASCADE)
    skill_name = models.CharField(max_length=100)
    proficiency_level = models.CharField(max_length=50, choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced'), ('Expert', 'Expert')])
    years_of_experience = models.IntegerField(null=True, blank=True)
    certification = models.CharField(max_length=200, null=True, blank=True)
    skill_type = models.CharField(max_length=50, choices=[('Technical', 'Technical'), ('Soft', 'Soft')], default='Technical')

    def __str__(self):
        return f"{self.skill_name} ({self.proficiency_level})"