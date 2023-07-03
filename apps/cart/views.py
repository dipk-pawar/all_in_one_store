from django.shortcuts import redirect, render
from apps.store.models import Product
from .models import Cart, CartItem


# Create your views here.
def cart(request):
    return render(request, "store/cart.html")


def _cart_id(requst):
    return requst.session.session_key or requst.session.create()


def add_cart(requst, product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(requst))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(requst))
        cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(product=product, cart=cart, quantity=1)
        cart_item.save()

    return redirect("cart")
