# authors/models.py
from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=255)
    total_rating = models.FloatField(default=0.0)
