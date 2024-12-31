from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'cover']

class FinishedBookEditForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'rating', 'finished_date']