from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import serializers

from main.models import Book, Author, Publisher, Review


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'name', 'surname', 'patronymic')


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ('id', 'name', 'address', 'city', 'country', 'website')


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    publisher = PublisherSerializer()

    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'description', 'published_date', 'publisher')


class WriteBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'description', 'published_date', 'publisher')

    def validate(self, attrs):
        title = attrs.get('title')
        description = attrs.get('description')
        if title:
            if not description and len(title) < 10:
                raise serializers.ValidationError('Название книги слишком короткое')
        return attrs

    def validate_published_date(self, value):
        if value > timezone.now().date():
            raise serializers.ValidationError('Дата публикации не может быть в будущем')
        return value


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class ReviewSerializer(serializers.ModelSerializer):
    book = BookSerializer()
    author = UserSerializer()

    class Meta:
        model = Review
        fields = ('id', 'title', 'text', 'book', 'author', 'created_at', 'updated_at')


class WriteReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'title', 'text', 'author', 'book')
        extra_kwargs = {"author": {"required": False, "allow_null": True}}
