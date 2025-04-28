from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    studies = models.CharField(max_length=255, blank=True)
    live_in = models.CharField(max_length=255, blank=True)
    form=models.CharField(max_length=255, blank=True)
    marride=models.CharField(max_length=255, blank=True)
    phone_num = models.CharField(max_length=15, blank=True)
    your_flower = models.CharField(max_length=255, blank=True)
    fb_link = models.CharField(max_length=255, blank=True)
    linkid_link = models.CharField(max_length=255, blank=True)
    instagram_link = models.CharField(max_length=255, blank=True)
    socialmeida_link = models.CharField(max_length=255, blank=True)
    github_link = models.CharField(max_length=255, blank=True)
    
    
    def __str__(self):
        return self.username