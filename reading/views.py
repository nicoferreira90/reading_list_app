from django.shortcuts import render, redirect
from django.views.generic import ListView

from .models import Book


class ReadingListView(ListView):
    model = Book
    template_name = "reading/reading_list.html"
    context_object_name = "book_list"

    def post(self, request, *args, **kwargs):
        # Handling form submission (basic way, without using ModelForm)
        book_title = request.POST.get("book-title")
        book_author = request.POST.get("book-author")

        if book_title and book_author: # if a new book is being added to the list
            new_book = Book(title=book_title, author=book_author)
            new_book.save()
        else: # if a book is being removed from the list
            Book.objects.get(pk=request.POST.get("book-pk")).delete()

        # Redirecting after form submission to prevent resubmission on page refresh
        return redirect('reading_list')  # Use the name of your URL pattern here