from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .forms import NewUserForm, ProfileForm
from django.contrib import messages
from django.contrib.auth.models import User


def register(request):
    """Register a new User"""
    if request.method != "POST":
        # Display a blank registration form for new user
        form = NewUserForm()
    else:
        # Process completed form
        form = NewUserForm(data=request.POST)

        if form.is_valid():
            user = form.save()
            # log in user and redirect to home page
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("dg_photography:index")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    # display a blank or invalid form
    context = {"form": form}
    return render(request, "registration/register.html", context)


def user_profile(request):
    """a page for user's to create their profile"""

    if request.method != "POST":
        # Display a blank profile form
        form = ProfileForm()
    else:
        form = ProfileForm(data=request.POST)

        if form.is_valid():
            new_profile = form.save(commit=False)
            new_profile.save()
            return redirect("dg_photography:index")

    context = {"form": form}
    return render(request, "registration/user_profile.html", context)
