from django.contrib import admin
from .models import Book

class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "book_owner", "order")

admin.site.register(Book, BookAdmin)

