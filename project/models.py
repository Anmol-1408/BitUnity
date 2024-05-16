from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Project(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(default = timezone.now)
    project_name = models.CharField(max_length=150,null = False)
    project_description = models.TextField(null = False)
    institute = models.CharField(max_length=150,null = False,default = "")
    university = models.CharField(max_length=150,null = True,default = "")
    project_url = models.URLField(max_length=300,null = False)

class Comment(models.Model):
    comment = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

class UserProfile(models.Model):
	user = models.OneToOneField(User, primary_key=True, verbose_name='user', related_name='profile', on_delete=models.CASCADE)
	name = models.CharField(max_length=30, blank=True, null=True)
	bio = models.TextField(max_length=500, blank=True, null=True)
	birth_date=models.DateField(null=True, blank=True)
	location = models.CharField(max_length=100, blank=True, null=True)
	picture = models.ImageField(upload_to='uploads/profile_pictures', default='uploads/profile_pictures/default_user.jpg', blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()

    

