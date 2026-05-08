from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter
from .views import OrderViewSet
from order_item.views import OrderItemViewSet

router = DefaultRouter()
router.register(r'', OrderViewSet, basename='order')

orders_router = NestedSimpleRouter(router, r'', lookup='order')
orders_router.register(r'items', OrderItemViewSet, basename='order-items')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(orders_router.urls)),
]