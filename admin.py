from django.contrib import admin

from .models import Book, Genre, Choices

admin.site.register(Book)
admin.site.register(Genre)