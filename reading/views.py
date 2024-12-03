from django.shortcuts import render
from django.views.generic import ListView

from .models import Book


class ReadingListView(ListView):
    model = Book
    template_name = "reading/reading_list.html"
    context_object_name = "book_list"

