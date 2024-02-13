from django.urls import path

from .views import (
    activate,
    forgotPassword,
    login_user,
    logout_user,
    register_user,
    resetPassword,
    resetpassword_validate,
)

urlpatterns = [
    path("register/", register_user, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path("activate/<uidb64>/<token>/", activate, name="activate"),
    path("forgotPassword/", forgotPassword, name="forgotPassword"),
    path(
        "resetpassword_validate/<uidb64>/<token>/",
        resetpassword_validate,
        name="resetpassword_validate",
    ),
    path("resetPassword/", resetPassword, name="resetPassword"),
]
