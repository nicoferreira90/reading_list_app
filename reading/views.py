from django.shortcuts import render, redirect
from django.views.generic import ListView
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


def add_book(request):
    title = request.POST.get('book-title')
    author = request.POST.get('book-author')
    Book.objects.create(title=title, author=author, book_owner=request.user)

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
