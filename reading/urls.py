from django.urls import path
from .views import ReadingListView, add_book, delete_book

urlpatterns = [
    path("", ReadingListView.as_view(), name="reading_page"),
]

htmx_urlpatterns = [
    path("add_book/", add_book, name="add_book"),
    path("delete_book/<int:pk>/", delete_book, name="delete_book")
]

urlpatterns += urlpatterns+htmx_urlpatterns