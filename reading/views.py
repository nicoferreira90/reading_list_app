from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, TemplateView
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin

from datetime import datetime

from .sorting_functions import reorder_books
from .models import Book
from .forms import BookForm, FinishedBookEditForm


class AboutPageView(TemplateView):
    template_name = "reading/about.html"


class ReadingListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = "reading/reading_page.html"
    context_object_name = "book_list"
    login_url = "account_login"

    def get_queryset(self):
        """Override the get_queryset method so that ReadingListView only displays books registered by the current user."""
        return Book.objects.filter(book_owner=self.request.user).filter(finished=False)

    def get_context_data(self, **kwargs):
        # Get the base context data from the parent class
        context = super().get_context_data(**kwargs)

        top_book = (
            Book.objects.filter(book_owner=self.request.user)
            .filter(finished=False)
            .first()
        )
        context["top_book"] = top_book
        context["finished_book_list"] = (
            Book.objects.filter(book_owner=self.request.user)
            .filter(finished=True)
            .order_by("-finished_date")
        )
        print(top_book)
        return context


class FinishedBookListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = "reading/review_page.html"
    context_object_name = "finished_book_list"
    login_url = "account_login"

    def get_queryset(self):
        """Override the get_queryset method so that ReadingListView only displays books registered by the current user."""
        return (
            Book.objects.filter(book_owner=self.request.user)
            .filter(finished=True)
            .order_by("-finished_date")
        )


class BookUpdateView(LoginRequiredMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = "reading/partials/book_update.html"
    login_url = "account_login"
    context_object_name = "book"

    def form_valid(self, form):
        if not self.request.FILES.get("cover"):
            form.instance.cover = self.get_object().cover
        else:
            form.instance.cover = self.request.FILES.get("cover")
        form.save()
        print("form valid")

        return render(
            self.request,
            "reading/partials/reading_page_content_partial.html",
            {
                "book_list": Book.objects.filter(book_owner=self.request.user).filter(
                    finished=False
                ),
                "top_book": Book.objects.filter(book_owner=self.request.user).first(),
                "finished_book_list": Book.objects.filter(book_owner=self.request.user)
                .filter(finished=True)
                .order_by("-finished_date"),
            },
        )


class EditFinishedBookView(LoginRequiredMixin, UpdateView):
    model = Book
    form_class = FinishedBookEditForm
    template_name = "reading/partials/edit_finished_book.html"
    login_url = "account_login"
    context_object_name = "book"

    def form_valid(self, form):
        form.save()

        context = {
            "finished_book_list": Book.objects.filter(book_owner=self.request.user)
            .filter(finished=True)
            .order_by("-finished_date"),
        }

        return render(self.request, "reading/partials/review_page_table.html", context)


@login_required
def add_book(request):
    title = request.POST.get("book-title")
    author = request.POST.get("book-author")

    if request.user.books:
        new_book_order = (
            len(Book.objects.filter(book_owner=request.user).filter(finished=False)) + 1
        )
    else:
        new_book_order = 1

    Book.objects.create(
        title=title, author=author, book_owner=request.user, order=new_book_order
    )

    context = {
        "top_book": Book.objects.filter(book_owner=request.user)
        .filter(finished=False)
        .first(),
        "book_list": Book.objects.filter(book_owner=request.user).filter(
            finished=False
        ),
        "finished_book_list": Book.objects.filter(book_owner=request.user)
        .filter(finished=True)
        .order_by("-finished_date"),
    }

    return render(
        request, "reading/partials/reading_page_content_partial.html", context
    )


@require_http_methods(["DELETE"])
@login_required
def delete_book(request, pk):
    Book.objects.filter(pk=pk).delete()

    # here we proceed to re-order the remaining books from 1 to n
    book_list = Book.objects.filter(book_owner=request.user).filter(finished=False)
    book_list = reorder_books(book_list)

    context = {
        "top_book": Book.objects.filter(book_owner=request.user)
        .filter(finished=False)
        .first(),
        "book_list": book_list,
        "finished_book_list": Book.objects.filter(book_owner=request.user)
        .filter(finished=True)
        .order_by("-finished_date"),
    }

    return render(
        request, "reading/partials/reading_page_content_partial.html", context
    )


@login_required
def book_search(request):
    search_text = request.POST.get("search")
    book_search_list = Book.objects.filter(
        Q(title__icontains=search_text) | Q(author__icontains=search_text)
    ).filter(book_owner=request.user)

    return render(
        request,
        "reading/partials/book_list_partial.html",
        {"book_list": book_search_list},
    )


@login_required
def book_sort(request):
    book_order = request.POST.getlist("book_order")
    index = 1
    for book in book_order:
        this_book = Book.objects.get(pk=book)
        if this_book.finished == False:
            this_book.order = index
            this_book.save()
            index += 1

    context = {
        "top_book": Book.objects.filter(book_owner=request.user)
        .filter(finished=False)
        .first(),
        "book_list": Book.objects.filter(book_owner=request.user).filter(
            finished=False
        ),
        "finished_book_list": Book.objects.filter(book_owner=request.user)
        .filter(finished=True)
        .order_by("-finished_date"),
    }

    return render(
        request, "reading/partials/reading_page_content_partial.html", context
    )


@login_required
def top_book_completed(request, pk):
    top_book = Book.objects.get(pk=pk)
    top_book.finished = True
    top_book.finished_date = datetime.now()
    top_book.save()

    book_list = Book.objects.filter(book_owner=request.user).filter(finished=False)
    book_list = reorder_books(book_list)

    context = {
        "top_book": Book.objects.filter(book_owner=request.user)
        .filter(finished=False)
        .first(),
        "book_list": Book.objects.filter(book_owner=request.user).filter(
            finished=False
        ),
        "finished_book_list": Book.objects.filter(book_owner=request.user)
        .filter(finished=True)
        .order_by("-finished_date"),
    }

    return render(
        request, "reading/partials/reading_page_content_partial.html", context
    )


@require_http_methods(["DELETE"])
@login_required
def delete_completed_book(request, pk):

    Book.objects.filter(pk=pk).delete()

    context = {
        "finished_book_list": Book.objects.filter(book_owner=request.user)
        .filter(finished=True)
        .order_by("-finished_date"),
    }

    return render(request, "reading/partials/review_page_table.html", context)
