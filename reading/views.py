from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.decorators.http import require_http_methods

from .models import Book


class ReadingListView(ListView):
    model = Book
    template_name = "reading/reading_page.html"
    context_object_name = "book_list"

def add_book(request):
    title = request.POST.get('book-title')
    author = request.POST.get('book-author')
    Book.objects.create(title=title, author=author)

    book_list = Book.objects.all()
    return render(request, 'reading/book_list.html', {'book_list': book_list})

@require_http_methods(['DELETE'])
def delete_book(request, pk):
    Book.objects.filter(pk=pk).delete()
    book_list = Book.objects.all()
    return render(request, 'reading/book_list.html', {'book_list': book_list})

