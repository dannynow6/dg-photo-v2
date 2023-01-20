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
    owner = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default="dan")

    def __str__(self) -> str:
        """Return a string representation of BlogArticle"""
        title = self.title.title()
        author = self.author.title()
        date = self.date_published
        return f"{author} | {title} | {date}"


class Comment(models.Model):
    """A user's comment about a blog article"""

    article = models.ForeignKey(BlogArticle, on_delete=models.CASCADE)
    comment = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "comments"

    def __str__(self):
        """return a string representation of model"""
        return f"{self.comment[:50]}..."
