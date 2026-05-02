from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from .models import Category
from .serializers import CategorySerializer

class CategoryViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]