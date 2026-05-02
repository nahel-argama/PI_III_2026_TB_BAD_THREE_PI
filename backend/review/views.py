from rest_framework import viewsets, mixins
from .serializers import ReviewSerializer
from .models import Review

class ReviewViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin):

    serializer_class = ReviewSerializer

    def get_queryset(self):
        user = self.request.user

        if hasattr(user, 'producer'):
            return Review.objects.filter(order__id__producer=self.request.user.id)

        return Review.objects.filter(order__retailer=self.request.user.retailer)