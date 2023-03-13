from django.shortcuts import redirect
from photo_blog.models import BlogArticle



def post_before_comment(view_func):
    """
    this decorator ensures a User creates a blog article before commenting on
    any articles
    """

    def wrapped_view(request, *args, **kwargs):
        # Get count of articles published by current user 
        user_article_count = BlogArticle.objects.filter(owner=request.user).count()
        # Check to see if current user has published at least 1 article 
        if user_article_count == 0:
            # if user has not published at least 1 article, redirect create new article
            return redirect("photo_blog:new_blog_article")
        return view_func(request, *args, **kwargs)

    return wrapped_view
