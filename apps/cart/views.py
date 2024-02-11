import contextlib

from django.shortcuts import get_object_or_404, redirect, render

from apps.store.models import Product, Variation

from .models import Cart, CartItem


# Create your views here.
def cart(request, total=0, quantity=0, cart_items=None):
    tax = 0
    grand_total = 0
    with contextlib.suppress(Cart.DoesNotExist):
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
            quantity += cart_item.quantity
        tax = (2 * total) / 100
        grand_total = total + tax

    return render(
        request,
        "store/cart.html",
        context={
            "total": total,
            "quantity": quantity,
            "cart_items": cart_items,
            "tax": tax,
            "grand_total": grand_total,
        },
    )


def _cart_id(request):
    return request.session.session_key or request.session.create()


def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    product_variations = []
    if request.method == "POST":
        for item in request.POST:
            item_key = item
            item_value = request.POST[item_key]
            with contextlib.suppress(Exception):
                variation = Variation.objects.get(
                    product=product,
                    variation_category__iexact=item_key,
                    variation_value__iexact=item_value,
                )
                product_variations.append(variation)

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()

    if _ := CartItem.objects.filter(product=product, cart=cart).exists():
        cart_item = CartItem.objects.filter(product=product, cart=cart)
        ex_var_list = []
        ids = []
        for item in cart_item:
            existing_variations = item.variations.all()
            ex_var_list.append(list(existing_variations))
            ids.append(item.id)

        if product_variations in ex_var_list:
            index_vr = ex_var_list.index(product_variations)
            item_id = ids[index_vr]
            item = CartItem.objects.get(product=product, id=item_id)
            item.quantity += 1
            item.save()
        else:
            item = CartItem.objects.create(product=product, cart=cart, quantity=1)
            if product_variations:
                item.variations.clear()
                item.variations.add(*product_variations)
            item.save()
    else:
        cart_item = CartItem.objects.create(product=product, cart=cart, quantity=1)
        if product_variations:
            cart_item.variations.clear()
            cart_item.variations.add(*product_variations)
        cart_item.save()

    return redirect("cart")


def remove_cart(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    with contextlib.suppress(Exception):
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    return redirect("cart")


def remove_cart_item(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    CartItem.objects.get(product=product, cart=cart, id=cart_item_id).delete()
    return redirect("cart")
