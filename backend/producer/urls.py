from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProducerViewSet

router = DefaultRouter()
router.register(r'', ProducerViewSet, basename='producer')

urlpatterns = [
    path('', include(router.urls)),
]