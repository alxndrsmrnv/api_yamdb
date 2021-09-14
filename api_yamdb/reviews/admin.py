from django.contrib import admin

from .models import Category, Comment, Genre, Profile, Review, Title

admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Genre)
admin.site.register(Title)
admin.site.register(Review)
