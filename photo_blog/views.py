from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import BlogArticle, Comment
from .forms import BlogArticleForm, CommentForm

# imports for reportlab example django docs
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# imports for styling purposes and PDF structure
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image

# from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.units import inch

# from reportlab.rl_config import defaultPageSize

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
    company_name = "G. Cotter Enterprises, Inc."
    address_parts = [
        "48 Brown Avenue",
        "Springfield, NJ 07081",
        "Phone: (973) 376-5840",
        "Fax: (973) 376-5937",
        "Toll free: (888) 808-WELD",
    ]

    styles = getSampleStyleSheet()
    p.setFont("Times-Roman", 16, leading=None)
    # Try using textobject to do address at bottom left of page
    textobject = p.beginText(50, 105)
    textobject.setFont("Times-Roman", 10, leading=None)
    textobject.textLine(text=company_name)
    p.drawText(textobject)
    textobject1 = p.beginText(65, 90)
    textobject1.setFont("Times-Roman", 10, leading=None)
    textobject1.textLine(text=address_parts[0])
    p.drawText(textobject1)
    textobject2 = p.beginText(55, 75)
    textobject2.setFont("Times-Roman", 10, leading=None)
    textobject2.textLine(text=address_parts[1])
    p.drawText(textobject2)
    textobject3 = p.beginText(54, 60)
    textobject3.setFont("Times-Roman", 10, leading=None)
    textobject3.textLine(text=address_parts[2])
    p.drawText(textobject3)
    textobject4 = p.beginText(58, 45)
    textobject4.setFont("Times-Roman", 10, leading=None)
    textobject4.textLine(text=address_parts[3])
    p.drawText(textobject4)
    # New Text Object for Signature area bottom-right page 
    textobj = p.beginText(335, 100)
    textobj.setFont("Times-Italic", 14, leading=None) 
    textobj.textLine(text=company_name) 
    p.drawText(textobj)
    textobj1 = p.beginText(335, 45)
    textobj1.setFont("Times-Roman", 10, leading=None) 
    textobj1.textLine(text="Jerry Cotter, President")
    p.drawText(textobj1)
    p.line(335, 65, 470, 65)
    # New text object for Cert of Compliance bottom info 
    cc_obj = p.beginText()
    # p.setFont("Times-Roman", 14, leading=None)
    # save page dimensions to variables width/height
    # width, height = letter
    # Grab article info and define variables to then draw on Canvas
    article = BlogArticle.objects.get(id=article_id)
    title = article.title.title()
    author = article.author.title()
    date_pub = str(article.date_published)
    description = article.description
    text = article.article

    # Draw things to the PDF - ie generate a PDF
    # p.setStrokeColorRGB(94, 94, 94)
    # p.line(248, 490, 350, 490)
    # p.rect(245, 390, 50, 25, stroke=1, fill=0)
    # p.circle(300, 500, 200, stroke=1, fill=0)
    """
    p.drawString(250, 500, title)
    p.drawString(250, 400, author)
    p.drawString(250, 300, date_pub)
    p.drawString(250, 200, description)
    # Trying some cotter stuff to see what it looks like
    object1 = p.beginText(400, 800)
    object1.setFont("Helvetica", 16, leading=None)
    object1.textLine(text="G. Cotter Enterprises, Inc.")

    p.drawString(100, 115, "G. Cotter Enterprises, Inc.")
    p.drawString(115, 100, "48 Brown Avenue")
    p.drawString(105, 85, "Springfield, NJ 07081")
    p.drawString(105, 70, "Phone: (973) 376-5840")
    p.drawString(110, 55, "Fax: (973) 376-5937")
    p.setFont("Times-Italic", 14, leading=None)
    p.drawString(400, 115, "G. Cotter Enterprises, Inc.")
    # p.drawCentredString(275, 100, text)"""

    # Close the PDF object cleanly, and we're done
    p.showPage()
    p.save()
    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f"{date_pub}.pdf")
