from django.shortcuts import render
from .models import Product


# Create your views here.
def home(request):
    products = Product.objects.filter(is_available=True)
    return render(request, "home.html", context={"products": products})
