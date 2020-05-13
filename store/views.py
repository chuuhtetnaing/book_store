import csv, io
from django.shortcuts import render, redirect
from django.contrib import messages
from store.models import Book

def home(request):
    books = Book.objects.all()[:30]
    for book in books:
        book.description = book.description[:100] + " ............"
    cart = request.session.get('cart')
    context = {"books": books, "cart": cart}
    return render(request, 'store/home.html', context)

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
    return redirect('home')

def remove_from_cart(request, book_id):
    context = {}
    orders = request.session.get('cart')
    orders.remove(str(book_id))
    request.session['cart'] = orders
    return redirect('store/cart_page')