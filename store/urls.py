from django.urls import path
from . import views

urlpatterns = [
    path("home", views.home, name="home"),
    path("view_cart", views.view_cart, name="cart_page"),
    path("add_to_cart/<int:book_id>", views.add_to_cart, name="add_to_cart"),
    path("remove_from_cart/<int:book_id>", views.remove_from_cart, name="remove_from_cart"),
]