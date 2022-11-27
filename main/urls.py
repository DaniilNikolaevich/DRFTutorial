from django.urls import path, include
from rest_framework.routers import DefaultRouter

from main import views


router = DefaultRouter()  # Создаем роутер
router.register('books', views.BookViewSet, basename='books')  # Регистрируем наш ViewSet
router.register('authors', views.AuthorViewSet, basename='authors')  # Регистрируем наш ViewSet
router.register('reviews', views.ReviewViewSet, basename='reviews')  # Регистрируем наш ViewSet

urlpatterns = [
    path('', include(router.urls)),
    # path('books', views.books),
    # path('books/<int:book_id>', views.book_detail),
    # path('books', views.BookView.as_view()),
    # path('books/<int:book_id>', views.BookDetailView.as_view()),

    # path('books', views.BookList.as_view()),
    # path('books/<int:book_id>', views.BookDetail.as_view()),
]
