from rest_framework.permissions import BasePermission

class IsProducer(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.user_type == 'PRODUCER'
        )

class IsRetailer(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.user_type == 'RETAILER'
        )