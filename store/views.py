import csv, io
from django.shortcuts import render
from django.contrib import messages
from store.models import Book

def home(request):
    books = Book.objects.all()[:30]
    for book in books:
        book.description = book.description[:100] + " ............"
    context = {"books": books}
    return render(request, 'store/home.html', context)