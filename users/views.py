# views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Author, Book, Review
from .serializers import AuthorSerializer, BookSerializer, ReviewSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import UserSerializer
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.authtoken.views import ObtainAuthToken
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from django.db.models import Avg, Sum


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def books(self, request, pk=None):
        author = self.get_object()
        books = Book.objects.filter(author=author)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def list_books(self, request):
        books = self.get_queryset()
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['put'])
    def update_book(self, request, pk=None):
        book = self.get_object()
        serializer = self.get_serializer(book, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        self.update_author_ratings(serializer.validated_data['author'])
        self.update_book_ratings(serializer.validated_data['book'])
        self.update_review_ratings(serializer.instance)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update_author_ratings(self, author):
        if author:
            avg_rating = author.reviews.all().aggregate(avg_rating=Avg('rating'))['avg_rating']
            print(f"Avg Rating for Author: {avg_rating}")
            author.total_rating = avg_rating
            author.save()

    def update_book_ratings(self, book):
        if book:
            print(f"Type of book: {type(book)}")
            avg_rating = book.reviews.all().aggregate(avg_rating=Avg('rating'))['avg_rating']
            print(f"Avg Rating for Book: {avg_rating}")
            book.total_rating = avg_rating
            book.save()
        
    def update_review_ratings(self, review):
        if review:
            print(f"Type of review: {type(review)}")
            existing_reviews = Review.objects.filter(author=review.author, book=review.book)
            total_ratings_sum = existing_reviews.aggregate(total_ratings_sum=Sum('rating'))['total_ratings_sum'] or 0
            total_ratings_count = existing_reviews.count()
            
            cumulative_average = (total_ratings_sum + review.rating) / (total_ratings_count + 1)

            review.total_rating = cumulative_average
            review.save()

    @action(detail=False, methods=['GET'])
    def author_reviews(self, request):
        author_id = request.query_params.get('author_id')
        if not author_id:
            return Response({"error": "Author ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        reviews = Review.objects.filter(author__id=author_id)
        serializer = self.get_serializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_user(request):
    print(request.data)
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        password = request.data.get('password')
        user.set_password(password)
        user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
