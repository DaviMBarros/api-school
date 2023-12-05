from rest_framework import permissions
from .models import Account
from rest_framework.views import Request, View


class AccountPermission(permissions.BasePermission):
    def has_object_permission(
        self,
        request: Request,
        view: View,
        obj: Account
    ):
        return request.user.is_authenticated and obj == request.user.is_superuser
