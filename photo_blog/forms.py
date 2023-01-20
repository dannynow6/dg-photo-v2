from django import forms
from .models import BlogArticle, Comment


class BlogArticleForm(forms.ModelForm):
    """A form for adding a new Article to Photo Blog"""

    class Meta:
        model = BlogArticle
        fields = [
            "title",
            "author",
            "image",
            "description",
            "article",
        ]
        labels = {
            "title": "Title",
            "author": "Author",
            "image": "Image",
            "description": "Description",
            "article": "Article",
        }
        widgets = {
            "title": forms.TextInput,
            "author": forms.TextInput,
            "image": forms.ClearableFileInput,
            "description": forms.TextInput,
            "article": forms.Textarea,
        }


class CommentForm(forms.ModelForm):
    """A form for adding a new comment to Photo Blog"""

    class Meta:
        model = Comment
        fields = [
            "comment",
        ]
        labels = {
            "comment": "Comment",
        }
        widgets = {"comment": forms.Textarea(attrs={"cols": 80})}
