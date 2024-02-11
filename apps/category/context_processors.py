from apps.cart.models import Cart, CartItem
from apps.cart.views import _cart_id

from .models import Category


def menu_links(request):
    links = Category.objects.all()
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item_count = CartItem.objects.filter(cart=cart).count()
    except Cart.DoesNotExist:
        cart_item_count = 0
    return dict(links=links, cart_item_count=cart_item_count)
