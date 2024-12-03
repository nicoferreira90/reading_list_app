from django.urls import path
from .views import ReadingListView

urlpatterns = [
    path("", ReadingListView.as_view(), name="reading_list"),
]
