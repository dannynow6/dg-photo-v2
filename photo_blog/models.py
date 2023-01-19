from django.db import models
from django.contrib.auth.models import User 


class BlogArticle(models.Model):
    """
    A model of a blog article
    """

    title = models.CharField(max_length=250, unique=True)
    author = models.CharField(max_length=250)
    image = models.ImageField(upload_to="photos/", blank=True)
    date_published = models.DateField(auto_now_add=True)
    description = models.CharField(max_length=300)
    article = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE) 

    def __str__(self) -> str:
        """Return a string representation of BlogArticle"""
        title = self.title.title()
        author = self.author.title()
        date = self.date_published
        return f"{author} | {title} | {date}"
