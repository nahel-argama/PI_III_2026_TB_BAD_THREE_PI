from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VarejistaViewSet

router = DefaultRouter()
router.register(r'', VarejistaViewSet, basename='varejista')

urlpatterns = [
    path('', include(router.urls)),
]