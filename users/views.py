from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.views import View
from django.http import HttpResponse
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken

from .forms import RegisterForm, LoginForm
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, "register.html", {"form": form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.is_active = False
            user.activation_code = get_random_string(32)
            user.save()

            activation_link = f"http://127.0.0.1:8000/auth/activate/?code={user.activation_code}&email={user.email}"

            send_mail(
                subject="Активация аккаунта",
                message=f"Перейдите по ссылке для активации: {activation_link}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
            )

            return HttpResponse(" Проверьте почту для активации аккаунта!")
        return render(request, "register.html", {"form": form})


def activate_account(request):
    email = request.GET.get("email")
    code = request.GET.get("code")

    try:
        user = User.objects.get(email=email, activation_code=code, is_active=False)
        user.is_active = True
        user.activation_code = None
        user.save()

      
        refresh = RefreshToken.for_user(user)
        response = redirect("home")
        response.set_cookie("access", str(refresh.access_token), httponly=True)
        response.set_cookie("refresh", str(refresh), httponly=True)
        return response

    except User.DoesNotExist:
        return HttpResponse("Неверный код или email")


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "login.html", {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, email=email, password=password)
            if user is not None and user.is_active:
                refresh = RefreshToken.for_user(user)
                response = redirect("home")
                response.set_cookie("access", str(refresh.access_token), httponly=True)
                response.set_cookie("refresh", str(refresh), httponly=True)
                return response
            return render(request, "login.html", {"form": form, "error": "Неверные данные или аккаунт не активирован"})
        return render(request, "login.html", {"form": form})