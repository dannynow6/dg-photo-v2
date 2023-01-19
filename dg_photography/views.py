from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import random

# from django.contrib.auth.decorators import login_required
from .models import Photo
from .forms import PhotoForm
from photo_blog.models import BlogArticle

# Main site page
def index(request):
    """The home page for dg_photography"""
    articles = BlogArticle.objects.all()
    x = random.randint(1, len(articles))
    article_id = x
    article = BlogArticle.objects.get(id=article_id)
    context = {"article": article}
    return render(request, "dg_photography/index.html", context)


@login_required
def new_photo(request):
    """New photo info submitted"""
    if request.method != "POST":
        form = PhotoForm()
    else:
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            new_photo = form.save(commit=False)
            new_photo.owner = request.user
            new_photo.save()
            return redirect("dg_photography:my_photos")

    context = {
        "form": form,
    }
    return render(request, "dg_photography/new_photo.html", context)


def about(request):
    """dg photography about page"""
    photos = Photo.objects.all()
    x = random.randint(1, len(photos))
    photo_id = x
    photo = Photo.objects.get(id=photo_id)
    context = {"photo": photo}
    return render(request, "dg_photography/about.html", context)


def photos(request):
    """dg photography page displaying photos uploaded to site"""
    photos = Photo.objects.order_by("year_taken")
    context = {"photos": photos}
    return render(request, "dg_photography/photos.html", context)


def photo(request, photo_id):
    """show a single photo and its details"""
    photo = Photo.objects.get(id=photo_id)
    context = {"photo": photo}
    return render(request, "dg_photography/photo.html", context)


@login_required
def my_photos(request):
    """Show all photos a user has created/submitted"""
    my_photos = Photo.objects.filter(owner=request.user).order_by("year_taken")
    context = {"my_photos": my_photos}
    return render(request, "dg_photography/my_photos.html", context)


@login_required
def edit_photo(request, photo_id):
    """User can edit their own photo"""
    photo = Photo.objects.get(id=photo_id)

    if request.method != "POST":
        form = PhotoForm(instance=photo)
    else:
        form = PhotoForm(request.POST, request.FILES, instance=photo)
        if form.is_valid():
            form.save()
            return redirect("dg_photography:my_photos")
    context = {"photo": photo, "form": form}
    return render(request, "dg_photography/edit_photo.html", context)
