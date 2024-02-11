from django.shortcuts import render

from apps.store.models import Product


# Create your views here.
def home_view(request):
    products = Product.objects.filter(is_available=True)
    return render(request, "home.html", context={"products": products})
