from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import BlogArticle, Comment
from .forms import BlogArticleForm, CommentForm

# imports for reportlab example django docs
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import datetime 
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


def print_article(request, article_id):
    # Create a file-like buffer to receive the PDF data
    buffer = io.BytesIO()
    # Create the PDF object using buffer as its 'file' / define pagesize as standard letter
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # logo = "../../img_fordoc/dg.png"
    # p.drawImage(logo, width * 0.4, height * 0.8, width=125, height=125)
    
    # p.setFont("Times-Roman", 14, leading=None)
    # save page dimensions to variables width/height
    # width, height = letter
    # Grab article info and define variables to then draw on Canvas
    article = BlogArticle.objects.get(id=article_id)
    title = article.title.title()
    author = article.author.title()
    date_pub = article.date_published  # use f"{date_pub.strftime('%m/%d/%Y')}""
    description = article.description
    text = article.article
    photo = article.image 
    # Add logo
    dg_logo = "./static/img/dg_logo.jpg" 
    p.drawImage(dg_logo, 198, 612, width=None, height=None) 
    # add title of article 
    title_obj = p.beginText(252, 576)
    title_obj.setFont("Times-BoldItalic", 14, leading=None) 
    title_obj.textLine(text=f"{title}") 
    p.drawText(title_obj) 
    # Add Date 
    date_obj = p.beginText(504, 540)
    date_obj.setFont("Times-Roman", 11, leading=None) 
    date_obj.textLine(text=f"{date_pub.strftime('%m/%d/%Y')}")
    p.drawText(date_obj) 
    # author 
    auth_obj = p.beginText(108, 504) 
    auth_obj.setFont("Times-Roman", 11, leading=None) 
    auth_obj.textLine(text=f"written by {author}")
    p.drawText(auth_obj)    
    # Close the PDF object cleanly, and we're done
    p.showPage()
    p.save()
    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f"{date_pub}.pdf")
