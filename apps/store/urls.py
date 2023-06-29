from apps.store.views import store
from django.urls import path

urlpatterns = [path("", store, name="store")]
