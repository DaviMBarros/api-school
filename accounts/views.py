from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import CreateAPIView
from .models import Account
from .serializers import AccountSerializer


class LoginJWTView(TokenObtainPairView):
    ...


class CreateAccount(CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
