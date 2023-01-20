from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import BlogArticle, Comment
from .forms import BlogArticleForm, CommentForm

# Create your views here


def photo_blog(request):
    """Basic landing page for Photo Blog Articles"""
    articles = BlogArticle.objects.order_by("-date_published")
    context = {"articles": articles}
    return render(request, "photo_blog/photo_blog.html", context)


@login_required
def new_blog_article(request):
    """New Blog Article Form"""
    if request.method != "POST":
        form = BlogArticleForm()
    else:
        form = BlogArticleForm(request.POST, request.FILES)
        if form.is_valid():
            new_article = form.save(commit=False)
            new_article.owner = request.user
            new_article.save()
            return redirect("photo_blog:my_articles")
    context = {
        "form": form,
    }
    return render(request, "photo_blog/new_blog_article.html", context)


def article(request, article_id):
    """Show a single article's contents and info"""
    article = BlogArticle.objects.get(id=article_id)
    comments = article.comment_set.order_by("-date_added")
    context = {"article": article, "comments": comments}
    return render(request, "photo_blog/article.html", context)


@login_required
def my_articles(request):
    """Show all articles created by current user"""
    my_articles = BlogArticle.objects.filter(owner=request.user).order_by(
        "-date_published"
    )
    context = {"my_articles": my_articles}
    return render(request, "photo_blog/my_articles.html", context)


@login_required
def edit_article(request, article_id):
    """User can edit an existing article"""
    article = BlogArticle.objects.get(id=article_id)

    if request.method != "POST":
        form = BlogArticleForm(instance=article)
    else:
        form = BlogArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect("photo_blog:my_articles")
    context = {"article": article, "form": form}
    return render(request, "photo_blog/edit_article.html", context)


@login_required
def new_comment(request, article_id):
    """Add a new comment for a particular article"""
    article = BlogArticle.objects.get(id=article_id)

    if request.method != "POST":
        # No data submitted - create blank form
        form = CommentForm()
    else:
        # POST data submitted; process data
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.article = article
            new_comment.owner = request.user
            new_comment.save()
            return redirect("photo_blog:article", article_id=article_id)
    # Display a blank or invalid form
    context = {"article": article, "form": form}
    return render(request, "photo_blog/new_comment.html", context)
