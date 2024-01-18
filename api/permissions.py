from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions


class IsStudentOrInstructor(permissions.BasePermission):
    def has_permissions(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)
