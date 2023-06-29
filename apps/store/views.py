from django.shortcuts import render
from .models import Product


# Create your views here.
def store(request):
    return render(request, "store/store.html")
