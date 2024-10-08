from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from apps.cart.models import CartItem
from apps.cart.views import _cart_id
from apps.category.models import Category

from .models import Product


# Create your views here.
def store(request, category_slug=None):
    page = request.GET.get("page")
    if category_slug is not None:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(
            category=category, is_available=True
        ).order_by("id")
    else:
        products = Product.objects.filter(is_available=True).order_by("id")

    paginator = Paginator(products, 6)
    paged_product = paginator.get_page(page)
    product_counts = products.count()

    return render(
        request,
        "store/store.html",
        context={"products": paged_product, "product_counts": product_counts},
    )


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(
            category__slug=category_slug, slug=product_slug
        )
        in_cart = CartItem.objects.filter(
            cart__cart_id=_cart_id(request), product=single_product
        ).exists()
    except Exception as e:
        raise e
    return render(
        request,
        "store/product_detail.html",
        context={"single_product": single_product, "in_cart": in_cart},
    )


def search(request):
    if "keyword" in request.GET:
        key_word = request.GET["keyword"]
        products = Product.objects.filter(
            description__icontains=key_word, product_name__icontains=key_word
        ).order_by("id")
    else:
        products = Product.objects.all().order_by("id")
    context = {"products": products, "product_counts": products.count()}
    return render(
        request,
        "store/store.html",
        context=context,
    )
