from django.contrib import admin
from .models import AboutMe, Address, Skill, Project, Education, Experience

# Register your models here.
admin.site.register(AboutMe)
admin.site.register(Address)
admin.site.register(Skill)
admin.site.register(Project)
admin.site.register(Education)
admin.site.register(Experience)
