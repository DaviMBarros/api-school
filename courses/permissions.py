from rest_framework import permissions
from rest_framework.views import View
from accounts.models import Account


class IsAccountPermission(permissions.BasePermission):
    def has_permission(self, request, view: View):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_superuser


class ContentPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Account):
        if (
            request.method in permissions.SAFE_METHODS and request.user in obj.course.students.all()
        ):
            return True
        return request.user.is_authenticated and request.user.is_superuser
