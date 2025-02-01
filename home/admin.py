from django.contrib import admin

# Register your models here.
from .models import Post, Like, Comment

admin.site.register(Post)

# Register the Like model
admin.site.register(Like)

# Register the Comment model
admin.site.register(Comment)