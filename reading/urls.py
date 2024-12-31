from django.urls import path
from .views import (
    ReadingListView,
    FinishedBookListView,
    BookUpdateView,
    add_book,
    delete_book,
    book_search,
    book_sort,
    top_book_completed,
    delete_completed_book,
    EditFinishedBookView,
)

urlpatterns = [
    path("", ReadingListView.as_view(), name="reading_page"),
    path("reviews/", FinishedBookListView.as_view(), name="review_page"),
]

htmx_urlpatterns = [
    path("add_book/", add_book, name="add_book"),
    path("delete_book/<int:pk>/", delete_book, name="delete_book"),
    path("book_search/", book_search, name="book_search"),
    path("book_sort/", book_sort, name="book_sort"),
    path("book_update/<int:pk>/", BookUpdateView.as_view(), name="book_update"),
    path("top_book_completed/<int:pk>/", top_book_completed, name="top_book_completed"),
    path(
        "delete_completed_book/<int:pk>/",
        delete_completed_book,
        name="delete_completed_book",
    ),
    path(
        "edit_finished_book/<int:pk>",
        EditFinishedBookView.as_view(),
        name="edit_finished_book",
    ),
]

urlpatterns += urlpatterns + htmx_urlpatterns
