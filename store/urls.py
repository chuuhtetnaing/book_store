from django.urls import path
from . import views

app_name = 'store'
urlpatterns = [
    path("", views.home, name="home"),
    path("store/view_cart", views.view_cart, name="cart_page"),
    path("store/add_to_cart/<int:book_id>", views.add_to_cart, name="add_to_cart"),
    path("store/remove_from_cart/<int:book_id>", views.remove_from_cart, name="remove_from_cart"),
]