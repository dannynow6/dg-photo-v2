from django.db import models
from django.contrib.auth.models import User 
from django.dispatch import receiver 
from django.db.models.signals import post_save 

class Profile(models.Model):
    """A profile model to extend Django's build in User model"""
    EXPERIENCE_CHOICES = [
        ("pro", "Professional"),
        ("ama", "Amateur"),
        ("hob", "Hobbyist"), 
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    bio = models.CharField(max_length=300, blank=True) 
    type_photographer = models.CharField(max_length=5, choices=EXPERIENCE_CHOICES, default="ama") 
    affiliations = models.CharField(max_length=250, blank=True) 
    # Called when a new user is saved to auto create a profile 
    @receiver(post_save, sender=User) 
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance) 
    # Saves the user profile info when the user is saved 
    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save() 
    # Defines a string representation of model 
    def __str__(self):
        bio = self.bio 
        photo_type = self.type_photographer 
        affiliations = self.affiliations 
        return f"{bio[:50]} {photo_type} photographer | {affiliations}"
    
    