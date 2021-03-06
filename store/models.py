from django.db import models

# Create your models here.

class Book(models.Model):
    isbn = models.CharField(max_length=100)
    text_reviews_count = models.IntegerField()
    asin = models.CharField(max_length=100)
    is_ebook = models.CharField(max_length=10)
    average_rating = models.CharField(max_length=10)
    kindle_asin = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    book_format = models.CharField(max_length=100)
    link = models.CharField(max_length=200)
    authors = models.CharField(max_length=500)
    publisher = models.CharField(max_length=200)
    num_pages = models.CharField(max_length=10)
    publication_day = models.CharField(max_length=100)
    isbn13 = models.CharField(max_length=100)
    publication_month = models.CharField(max_length=100)
    publication_year = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    image_url = models.CharField(max_length=200)
    book_id = models.CharField(max_length=100)
    ratings_count = models.CharField(max_length=10)
    work_id = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    title_without_series = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.title}"

class Genre(models.Model):
    books = models.ManyToManyField(Book, related_name="genres")
    genre = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.genre}"