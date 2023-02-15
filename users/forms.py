from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.contrib.auth.models import User


class NewUserForm(UserCreationForm):
    """A custom new user form that extends the built-in Django usercreationform"""

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        )

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    EXPERIENCE_CHOICES = [
        ("pro", "Professional"),
        ("ama", "Amateur"),
        ("hob", "Hobbyist"),
    ]
    class Meta:
        model = Profile
        fields = ("bio", "type_photographer", "affiliations")
        labels = {
            "bio": "Bio",
            "type_photographer": "Type of Photographer",
            "affiliations": "Affiliations",
        }
        choices = {
            "type_photographer": "EXPERIENCE_CHOICES", 
        }
