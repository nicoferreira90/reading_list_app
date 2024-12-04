from django.urls import path
from .views import ReadingListView, add_book, delete_book, book_search

urlpatterns = [
    path("", ReadingListView.as_view(), name="reading_page"),
]

htmx_urlpatterns = [
    path("add_book/", add_book, name="add_book"),
    path("delete_book/<int:pk>/", delete_book, name="delete_book"),
    path("book_search/", book_search, name="book_search"),
]

urlpatterns += urlpatterns+htmx_urlpatterns