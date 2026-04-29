from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemPedidoViewSet
router = DefaultRouter()
router.register(r'', ItemPedidoViewSet, basename='item_pedido')

urlpatterns = [
    path('', include(router.urls)),
]




