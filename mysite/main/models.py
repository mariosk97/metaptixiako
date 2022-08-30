from django.db import models
#from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    has_applied = models.BooleanField(default=False)

class Application(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, null=True) #change null=True
    name = models.CharField(max_length=200) #application name, delete later
    description = models.TextField(null=True, blank=True) #delete later
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True) #time created should be when has_applied=True
    
    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name

