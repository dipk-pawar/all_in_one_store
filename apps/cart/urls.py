from .views import cart, add_cart
from django.urls import path

urlpatterns = [
    path("", cart, name="cart"),
    path("add_cart/<int:product_id>/", add_cart, name="add_cart"),
]
