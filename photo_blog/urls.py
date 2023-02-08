""" Defines URLs for photo_blog """
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = "photo_blog"
urlpatterns = [
    # A landing page for photo_blog
    path("photo_blog/", views.photo_blog, name="photo_blog"),
    # A page for submitting a new blog article
    path("new_blog_article/", views.new_blog_article, name="new_blog_article"),
    # A Page for Single Article Contents
    path("photo_blog/<int:article_id>/", views.article, name="article"),
    # A Page to display articles user has created
    path("my_articles/", views.my_articles, name="my_articles"),
    # A Page for users to edit their articles
    path("edit_article/<int:article_id>/", views.edit_article, name="edit_article"),
    # A page for adding a new comment
    path("new_comment/<int:article_id>/", views.new_comment, name="new_comment"),
    # A path for generating a pdf from an article
    path(
        "photo_blog/<int:article_id>/print/", views.print_article, name="print_article"
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
