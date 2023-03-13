# import functools
from django.shortcuts import redirect

# from django.contrib import messages
from photo_blog.models import BlogArticle

# from django.contrib.auth.models import User


def post_before_comment(view_func):
    """
    this decorator ensures a User creates a blog article before commenting on
    any articles
    """

    def wrapped_view(request, *args, **kwargs):
        user_article_count = BlogArticle.objects.filter(owner=request.user).count()
        if user_article_count == 0:
            return redirect("photo_blog:new_blog_article")
        return view_func(request, *args, **kwargs)

    return wrapped_view
