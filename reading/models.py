from django.db import models
from django.contrib.auth import get_user_model

class Book(models.Model):
    
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    book_owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="books")

    def __str__(self):
        return self.title
    