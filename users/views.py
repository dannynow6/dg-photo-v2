from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .forms import UserForm, ProfileForm


def register(request):
    """Register a new User"""
    if request.method != "POST":
        # Display a blank registration form for new user
        form = UserCreationForm()
    else:
        # Process completed form
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            # log in user and redirect to home page
            login(request, new_user)
            return redirect("dg_photography:index")
    # display a blank or invalid form
    context = {"form": form}
    return render(request, "registration/register.html", context)


def userpage(request):
    user_form = UserForm(instance=request.user)
    profile_form = ProfileForm(instance=request.user.profile)
    context = {
        "user": request.user,
        "user_form": user_form,
        "profile_form": profile_form,
    }
    return render(request=request, template_name="users/user.html", context=context)
