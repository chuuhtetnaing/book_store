import csv, io
import os
from django.shortcuts import render, redirect
from django.contrib import messages
from store.models import Book, Genre
from django.core.paginator import Paginator
from joblib import load
from django.conf import settings

loaded_rules = load(os.path.join(settings.BASE_DIR, 'rules.sav'))

def home(request):
    context = {}
    return render(request, 'store/home.html', context)


def books(request, genre):

    if request.method == 'POST':
        book_name = request.POST['book_name']
        books = Book.objects.filter(title__contains=book_name).values()
        genre = f"Title Contains '{book_name}'"
    else:
        if genre == 'all':
            books = Book.objects.all()
        else:
            genre = Genre.objects.get(genre=genre)
            books = genre.books.all()

    paginator = Paginator(books, 12)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    cart = request.session.get('cart')

    context = {'page_obj': page_obj, "cart": cart, "genre": genre}
    return render(request, 'store/books.html', context)

def view_book(request, book_id):
    cart = request.session.get('cart')
    book = Book.objects.get(book_id=book_id)
    recommendation_book_id = [list(x) for x in list(loaded_rules[(loaded_rules['antecedents'] == {book_id}) & (loaded_rules['consequents_len'] == 1)].sort_values(by=['lift'], ascending=False)['consequents'][:3])]
    recommendation_books = list()
    for book_id in recommendation_book_id:
        recommendation_books.append(Book.objects.get(book_id=book_id[0]))
    context = {"book": book, 'recommendation_books': recommendation_books, "cart": cart}
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

def checkout(request):
    if not request.user.is_authenticated:
        return redirect('account:login')
    cart = request.session.get('cart')
    orders = list()
    if not cart:
        return render(request, 'store/checkout.html', {"cart": cart}) 
    for book_id in cart:
        orders.append(Book.objects.get(book_id=book_id))
    context = {"cart": orders}
    return render(request, 'store/checkout.html', context)