from django.db import models
from django.contrib.auth.models import User 

class Profile(models.Model):
    """A profile model to extend Django's build in User model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    first_name = models.CharField(max_length=75)
    last_name = models.CharField(max_length=75)
    email = models.EmailField(max_length=300, unique=True) 
    
    def __str__(self):
        first = self.first_name 
        last = self.last_name 
        email = self.email 
        return f"{first.title()} {last.title()} | {email}"
    
    