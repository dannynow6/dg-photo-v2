from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import random

# from django.contrib.auth.decorators import login_required
from .models import Photo, PhotoComment
from .forms import PhotoForm, PhotoCommentForm
from photo_blog.models import BlogArticle

# Main site page
def index(request):
    """The home page for dg_photography"""
    articles = BlogArticle.objects.all()
    x = random.randint(1, len(articles))
    if x == 3:
        x += 1
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
    y = random.randint(1, len(photos))
    photo_id = x
    photo2_id = y
    photo = Photo.objects.get(id=photo_id)
    photo2 = Photo.objects.get(id=photo2_id)
    context = {"photo": photo, "photo2": photo2}
    return render(request, "dg_photography/about.html", context)


def photos(request):
    """dg photography page displaying photos uploaded to site"""
    photos = Photo.objects.order_by("-year_taken")
    context = {"photos": photos}
    return render(request, "dg_photography/photos.html", context)


def photo(request, photo_id):
    """show a single photo and its details"""
    photo = Photo.objects.get(id=photo_id)
    comments = photo.photocomment_set.order_by("-date_added")
    context = {"photo": photo, "comments": comments}
    return render(request, "dg_photography/photo.html", context)


@login_required
def my_photos(request):
    """Show all photos a user has created/submitted"""
    my_photos = Photo.objects.filter(owner=request.user).order_by("-year_taken")
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


@login_required
def new_photo_comment(request, photo_id):
    """Add a new comment for a particular photo"""
    photo = Photo.objects.get(id=photo_id)

    if request.method != "POST":
        # No data submitted - create blank form
        form = PhotoCommentForm()
    else:
        # POST data submitted; process data
        form = PhotoCommentForm(request.POST)
        if form.is_valid():
            new_photo_comment = form.save(commit=False)
            new_photo_comment.photo = photo
            new_photo_comment.owner = request.user
            new_photo_comment.save()
            return redirect("dg_photography:photo", photo_id=photo_id)
    # Display a blank or invalid form
    context = {"photo": photo, "form": form}
    return render(request, "dg_photography/new_photo_comment.html", context)
