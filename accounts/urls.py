from django.urls import path
from .views import LoginJWTView, CreateAccount

urlpatterns = [
    path("accounts/", CreateAccount.as_view()),
    path("login/", LoginJWTView.as_view())
]
