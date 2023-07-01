from apps.store.views import store
from django.urls import path

urlpatterns = [
    path("", store, name="store"),
    path("<slug:category_slug>", store, name="product_with_category"),
]
