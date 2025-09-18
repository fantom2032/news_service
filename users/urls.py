from django.urls import path
from .views import RegisterView, LoginView, activate_account

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("activate/", activate_account, name="activate"),
]
