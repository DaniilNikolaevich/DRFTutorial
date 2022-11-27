# Create your models here.
from django.contrib.auth.models import User
from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=30, verbose_name="Название издательства")
    address = models.CharField(max_length=50, verbose_name="Адрес издательства")
    city = models.CharField(max_length=60, verbose_name="Город издательства", null=True, blank=True)
    country = models.CharField(max_length=50, verbose_name="Страна издательства", null=True, blank=True)
    website = models.URLField(verbose_name="Сайт издательства", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название книги")
    author = models.ForeignKey(Author,
                               on_delete=models.CASCADE,
                               related_name="written_books",
                               verbose_name="Автор книги")
    description = models.TextField(verbose_name="Описание книги", null=True, blank=True)
    published_date = models.DateField(verbose_name="Дата публикации")
    publisher = models.ForeignKey(Publisher,
                                  on_delete=models.SET_NULL,
                                  related_name="published_books",
                                  verbose_name="Издательство", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return self.title


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews", verbose_name="Книга")
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name="reviews",
                               verbose_name="Автор отзыва")
    title = models.CharField(max_length=255, verbose_name="Заголовок отзыва")
    text = models.TextField(verbose_name="Текст отзыва")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return self.title
