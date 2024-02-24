from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import AuthorViewSet, BookViewSet, ReviewViewSet
from .views import create_user


router = DefaultRouter()
router.register(r'authors', AuthorViewSet, basename='author')
router.register(r'books', BookViewSet, basename='book')
router.register(r'reviews', ReviewViewSet, basename='review')

urlpatterns = [
    path('api/token/', obtain_auth_token, name='token_obtain_pair'),
    path('create_user/', create_user, name='create_user'),
    path('', include(router.urls)),
    
]