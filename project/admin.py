from django.contrib import admin
from .models import Project, Comment, UserProfile

# Register your models here.

admin.site.register(Project)
admin.site.register(Comment)
admin.site.register(UserProfile)
