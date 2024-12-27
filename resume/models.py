from django.db import models
from api.models import User

# Create your models here.

class AboutMe(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='about_me')
    full_name = models.CharField(max_length=255)
    position = models.CharField(max_length=20)
    about = models.TextField(blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.full_name


class Address(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='address')
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.street}, {self.city}"


class Skill(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='skill')
    title = models.CharField(max_length=100)
    soft_skills = models.TextField(blank=True, null=True)
    communication_skills = models.TextField(blank=True, null=True)
    other_skills = models.TextField(blank=True, null=True)


    def __str__(self):
        return self.title


class Project(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    technologies_used = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.title


class Education(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='education')
    degree = models.CharField(max_length=100)
    institution = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    grade = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.degree} - {self.institution}"


class Experience(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='experience')
    job_title = models.CharField(max_length=100)
    company_name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    responsibilities = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.job_title} at {self.company_name}"