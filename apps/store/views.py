from django.shortcuts import get_object_or_404, render
from .models import Product
from apps.category.models import Category


# Create your views here.
def store(request, category_slug=None):
    if category_slug is not None:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category, is_available=True)
    else:
        products = Product.objects.all()
    product_counts = products.count()
    return render(
        request,
        "store/store.html",
        context={"products": products, "product_counts": product_counts},
    )


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(
            category__slug=category_slug, slug=product_slug
        )
    except Exception as e:
        raise e
    return render(
        request, "store/product_detail.html", context={"single_product": single_product}
    )
