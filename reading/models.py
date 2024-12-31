from django.db import models
from django.contrib.auth import get_user_model

class Book(models.Model):
    
    title = models.CharField(max_length=75)
    author = models.CharField(max_length=75)
    book_owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="books")
    order = models.PositiveSmallIntegerField()
    cover = models.ImageField(upload_to="covers/", blank=True, null=True)

    # this are new
    finished = models.BooleanField(default=False)
    finished_date = models.DateTimeField(blank=True, null=True)
    review = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title