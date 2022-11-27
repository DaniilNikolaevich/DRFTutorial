from django.shortcuts import render
from rest_framework import generics, viewsets, mixins
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import Book, Author, Review
from main.permissions import IsAuthor
from main.serializers import BookSerializer, WriteBookSerializer, AuthorSerializer, ReviewSerializer, \
    WriteReviewSerializer


@api_view(['GET', 'POST'])
def books(request):
    if request.method == 'GET':
        all_books = Book.objects.all()
        data = BookSerializer(all_books, many=True).data
        return Response(data, status=200)
    else:
        serializer = WriteBookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def book_detail(request, book_id):
    if request.method == 'GET':
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({"message": "Книга не найдена"}, status=404)
        data = BookSerializer(book).data
        return Response(data, status=200)
    elif request.method == 'PUT':
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({"message": "Книга не найдена"}, status=404)
        serializer = WriteBookSerializer(instance=book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=204)
        return Response(serializer.errors, status=400)
    elif request.method == 'PATCH':
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({"message": "Книга не найдена"}, status=404)
        serializer = WriteBookSerializer(instance=book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=204)
        return Response(serializer.errors, status=400)
    elif request.method == 'DELETE':
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({"message": "Книга не найдена"}, status=404)
        book.delete()
        return Response(status=204)


class BookView(APIView):
    def get(self, request):
        all_books = Book.objects.all()
        data = BookSerializer(all_books, many=True).data
        return Response(data, status=200)

    def post(self, request):
        serializer = WriteBookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class BookDetailView(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request, book_id):
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({"message": "Книга не найдена"}, status=404)
        data = BookSerializer(book).data
        return Response(data, status=200)

    def put(self, request, book_id):
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({"message": "Книга не найдена"}, status=404)
        serializer = WriteBookSerializer(instance=book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=204)
        return Response(serializer.errors, status=400)

    def patch(self, request, book_id):
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({"message": "Книга не найдена"}, status=404)
        serializer = WriteBookSerializer(instance=book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=204)
        return Response(serializer.errors, status=400)

    def delete(self, request, book_id):
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({"message": "Книга не найдена"}, status=404)
        book.delete()
        return Response(status=204)


class BookList(generics.ListCreateAPIView):
    queryset = Book.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BookSerializer
        return WriteBookSerializer


class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    lookup_url_kwarg = 'book_id'

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BookSerializer
        return WriteBookSerializer

    def perform_update(self, serializer):
        print("Я вызвался до того, как объект был сохранен")
        serializer.save()
        print("Я вызвался после того, как объект был сохранен")

    def perform_destroy(self, instance):
        print("Я вызвался до того, как объект был удален")
        instance.delete()
        print("Я вызвался после того, как объект был удален")


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return BookSerializer
        return WriteBookSerializer

    def get_serializer_context(self):
        print(self.request.user, "USER")
        return {'request': self.request}


class CustomViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):
    pass


class AuthorViewSet(CustomViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    permission_classes = [IsAuthor]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ReviewSerializer
        return WriteReviewSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
