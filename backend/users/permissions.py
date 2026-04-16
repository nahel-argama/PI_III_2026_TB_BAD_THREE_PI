from rest_framework.permissions import BasePermission

class IsProdutor(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.type == 'PRODUTOR'
        )

class IsVarejista(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.type == 'VAREJISTA'
        )