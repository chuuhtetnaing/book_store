import csv, io
from django.shortcuts import render, redirect
from django.contrib import messages
from store.models import Book, Genre
from django.core.paginator import Paginator

def books(request, genre):
    if genre == 'all':
        books = Book.objects.all()
    else:
        genre = Genre.objects.get(genre=genre)
        books = genre.books.all()

    paginator = Paginator(books, 12)
    requested_genre = request.GET.get('genre')

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    cart = request.session.get('cart')
    context = {'page_obj': page_obj, "cart": cart, "genre": genre}
    return render(request, 'store/home.html', context)

def view_book(request, book_id):
    book = Book.objects.get(book_id=book_id)
    context = {"book": book}
    return render(request, 'store/book_detail.html', context)

def view_cart(request):
    cart = request.session.get('cart')
    orders = list()
    if not cart:
        return render(request, 'store/cart.html', {"cart": cart}) 
    for book_id in cart:
        orders.append(Book.objects.get(book_id=book_id))
    context = {"cart": orders}
    return render(request, 'store/cart.html', context)

def add_to_cart(request, book_id):
    context = {}
    if request.session.get('cart') is None:
        request.session['cart'] = []
    # return render(request, 'store/cart.html', context)
    orders = request.session.get('cart')
    orders.append(str(book_id))
    request.session['cart'] = orders
    return redirect('store:books', 'all')

def remove_from_cart(request, book_id):
    context = {}
    orders = request.session.get('cart')
    orders.remove(str(book_id))
    request.session['cart'] = orders
    return redirect('store:cart_page')