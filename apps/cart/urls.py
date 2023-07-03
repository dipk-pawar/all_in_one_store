from .views import cart
from django.urls import path

urlpatterns = [
    path("", cart, name="cart"),
]
