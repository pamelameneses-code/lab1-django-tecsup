from django.contrib import admin
from .models import Author, AuthorProfile, Book, Category, Publisher, Publication

admin.site.register(Author)
admin.site.register(AuthorProfile)
admin.site.register(Book)
admin.site.register(Category)
admin.site.register(Publisher)
admin.site.register(Publication)