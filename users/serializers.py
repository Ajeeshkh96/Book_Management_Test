from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Author, Book, Review


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
    books_count = serializers.SerializerMethodField()

    class Meta:
        model = Author
        fields = ('id', 'user', 'name', 'total_rating', 'books_count')

    def get_books_count(self, author):
        return author.book_set.count()