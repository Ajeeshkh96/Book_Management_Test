# books/models.py
from django.db import models
from authors.models import Author

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    total_rating = models.FloatField(default=0.0)
