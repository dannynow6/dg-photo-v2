""" Defines URL patterns for dg_photography """
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = "dg_photography"
urlpatterns = [
    # Home Page
    path("", views.index, name="index"),
    # New Photo Form
    path("new_photo/", views.new_photo, name="new_photo"),
    # A landing page for Dan G's Photography Website
    # path("dg_photos/", views.dg_photos, name="dg_photos"),
    # About page for dg photography
    path("about/", views.about, name="about"),
    # page for photos uploaded to site
    path("photos/", views.photos, name="photos"),
    # page for viewing individual photo details
    path("photos/<int:photo_id>/", views.photo, name="photo"),
    # A page displaying all photos submitted by user
    path("my_photos/", views.my_photos, name="my_photos"),
    # A page for a user to edit their photo
    path("edit_photo/<int:photo_id>/", views.edit_photo, name="edit_photo"),
    # A page for adding a new comment to photo
    path(
        "new_photo_comment/<int:photo_id>/",
        views.new_photo_comment,
        name="new_photo_comment",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
