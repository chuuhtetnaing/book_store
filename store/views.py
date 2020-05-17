import csv, io
import os
from django.shortcuts import render, redirect
from django.contrib import messages
from store.models import Book, Genre
from django.core.paginator import Paginator
from joblib import load
from django.conf import settings
from surprise import dump

mba_rules = load(os.path.join(settings.BASE_DIR, 'rules.sav'))
_, cf_item_to_item = dump.load(os.path.join(settings.BASE_DIR, 'cf_item_to_item.sav'))

def home(request):
    context = {}
    return render(request, 'store/home.html', context)


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
    
    itemset1_recommendation_book_id = [list(x) for x in list(mba_rules[(mba_rules['antecedents'] == {book_id}) & (mba_rules['consequents_len'] == 1)].sort_values(by=['lift'], ascending=False)['consequents'][:3])]
    
    if itemset1_recommendation_book_id:
        itemset1_recommendation_books = list()
        for id in itemset1_recommendation_book_id:
            itemset1_recommendation_books.append(Book.objects.get(book_id=id[0]))
    else:
        itemset1_recommendation_books = None

    check_len = [list(x) for x in list(mba_rules[(mba_rules['antecedents'] == {book_id}) & (mba_rules['consequents_len'] == 3)].sort_values(by=['lift'], ascending=False)['consequents'][:3])]
    if len(check_len) == 3:
        itemset3_recommendation_book_id = [list(x) for x in list(mba_rules[(mba_rules['antecedents'] == {book_id}) & (mba_rules['consequents_len'] == 3)].sort_values(by=['lift'], ascending=False)['consequents'][2:3])][0]
    elif len(check_len) == 2:
        itemset3_recommendation_book_id = [list(x) for x in list(mba_rules[(mba_rules['antecedents'] == {book_id}) & (mba_rules['consequents_len'] == 3)].sort_values(by=['lift'], ascending=False)['consequents'][1:2])][0]
    elif len(check_len) == 1:
        itemset3_recommendation_book_id = [list(x) for x in list(mba_rules[(mba_rules['antecedents'] == {book_id}) & (mba_rules['consequents_len'] == 3)].sort_values(by=['lift'], ascending=False)['consequents'][:1])][0]
    else:
        itemset3_recommendation_book_id = None

    if itemset3_recommendation_book_id:
        itemset3_recommendation_books = list()
        for id in itemset3_recommendation_book_id:
            itemset3_recommendation_books.append(Book.objects.get(book_id=id))
    else:
        itemset3_recommendation_books = None

    book_inner_id = cf_item_to_item.trainset.to_inner_iid(book_id)
    current_book_neighbors = cf_item_to_item.get_neighbors(book_inner_id, k=3)
    current_book_neighbors = [Book.objects.get(book_id=cf_item_to_item.trainset.to_raw_iid(inner_id)) for inner_id in current_book_neighbors]

    context = {"book": book, 'itemset1_recommendation_books': itemset1_recommendation_books, 'itemset3_recommendation_books': itemset3_recommendation_books, 'item_to_item_recommendation_books': current_book_neighbors, "cart": cart}
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