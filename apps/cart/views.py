import contextlib
from django.shortcuts import redirect, render
from apps.store.models import Product
from .models import Cart, CartItem


# Create your views here.
def cart(request, total=0, quantity=0, cart_items=None):
    with contextlib.suppress(Cart.DoesNotExist):
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
            quantity += cart_item.quantity
    return render(
        request,
        "store/cart.html",
        context={"total": total, "quantity": quantity, "cart_items": cart_items},
    )


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
