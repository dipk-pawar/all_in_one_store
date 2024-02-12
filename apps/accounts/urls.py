from django.urls import path

from .views import activate, login_user, logout_user, register_user

urlpatterns = [
    path("register/", register_user, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path("activate/<uidb64>/<token>/", activate, name="activate"),
]
