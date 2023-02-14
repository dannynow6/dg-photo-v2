from django import forms
from .models import Profile
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")
        labels = {
            "username": "Username",
            "first_name": "First Name",
            "last_name": "Last Name",
            "email": "Email",
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("bio", "type_photographer", "affiliations")
        labels = {
            "bio": "Bio",
            "type_photographer": "Type of Photographer",
            "affiliations": "Affiliations",
        }
