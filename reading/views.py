from django.shortcuts import render, redirect
from django.views.generic import ListView, UpdateView
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Book


class ReadingListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = "reading/reading_page.html"
    context_object_name = "book_list"
    login_url = "account_login"

    def get_queryset(self):
        """Override the get_queryset method so that ReadingListView only displays books registered by the current user."""
        return Book.objects.filter(book_owner=self.request.user)

class BookUpdateView(LoginRequiredMixin, UpdateView):
    model = Book
    template_name = "reading/partials/book_detail.html"

def add_book(request):
    title = request.POST.get('book-title')
    author = request.POST.get('book-author')

    if request.user.books:
        new_book_order = len(Book.objects.filter(book_owner=request.user))+1
    else:
        new_book_order = 1

    Book.objects.create(title=title, author=author, book_owner=request.user, order=new_book_order)

    book_list = Book.objects.filter(book_owner=request.user)
    return render(request, 'reading/partials/book_list.html', {'book_list': book_list})

@require_http_methods(['DELETE'])
def delete_book(request, pk):
    Book.objects.filter(pk=pk).delete()
    book_list = Book.objects.filter(book_owner=request.user)
    return render(request, 'reading/partials/book_list.html', {'book_list': book_list})

def book_search(request):
    search_text = request.POST.get("search")
    book_search_list = Book.objects.filter( Q(title__icontains=search_text) | Q(author__icontains=search_text) ).filter(book_owner=request.user)

    return render(request, 'reading/partials/book_list.html', {'book_list': book_search_list})

def book_sort(request):
    book_order = request.POST.getlist("book_order")
    index = 1
    for book in book_order:
        this_book = Book.objects.get(pk=book)
        this_book.order = index
        this_book.save()
        index += 1
    
    return render(request, "reading/partials/book_list.html", {"book_list": Book.objects.filter(book_owner=request.user)})