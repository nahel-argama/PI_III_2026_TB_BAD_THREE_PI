from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProdutorViewSet

router = DefaultRouter()
router.register(r'', ProdutorViewSet, basename='produtor')

urlpatterns = [
    path('', include(router.urls)),
]