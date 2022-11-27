from django.contrib import admin

from main.models import Author, Publisher, Book, Review

# Register your models here.

admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(Book)
admin.site.register(Review)
