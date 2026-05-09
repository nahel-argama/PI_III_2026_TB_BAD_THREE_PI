from rest_framework.permissions import BasePermission
from users.models import User


class IsProducer(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.user_type == User.USER_TYPE_PRODUCER
        )


class IsRetailer(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.user_type == User.USER_TYPE_RETAILER
        )
