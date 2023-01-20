from django.contrib import admin
from .models import BlogArticle, Comment

# Register your models here.
admin.site.register(BlogArticle)
admin.site.register(Comment) 
