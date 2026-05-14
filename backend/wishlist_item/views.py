from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import exceptions
from django.db import transaction

from product import price_scrapper_client
from product.price_scrapper_client import ExternalServiceError
from retailer.models import Retailer
from users.permissions import IsRetailer
from wishlist_item.filters import WishlistItemFilter
from wishlist.models import Wishlist
from wishlist_item.models import WishlistItem
from default_product_image.models import DefaultProductImage
from wishlist_item.serializers import WishlistItemSerializer


class BaseWishlistItemView(APIView):
    permission_classes = [IsRetailer]

    def get_wishlist(self, request):
        try:
            retailer = request.user.retailer
        except (AttributeError, Retailer.DoesNotExist):
            return None

        try:
            return Wishlist.objects.get(retailer=retailer)
        except Wishlist.DoesNotExist:
            return None


class WishlistItemListCreateView(BaseWishlistItemView):
    pagination_class = PageNumberPagination
    filterset_class = WishlistItemFilter

    def get(self, request):
        wishlist = self.get_wishlist(request)

        if not wishlist:
            return Response(
                {"detail": "Wishlist not found."}, status=status.HTTP_404_NOT_FOUND
            )

        queryset = WishlistItem.objects.filter(wishlist=wishlist).order_by("id")

        filterset = self.filterset_class(
            data=request.query_params, queryset=queryset, request=request
        )

        queryset = filterset.qs

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)

        serializer = WishlistItemSerializer(
            page, many=True, context={"request": request, "wishlist": wishlist}
        )

        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        wishlist = self.get_wishlist(request)
        if not wishlist:
            return Response(
                {"detail": "Wishlist not found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = WishlistItemSerializer(
            data=request.data, context={"request": request, "wishlist": wishlist}
        )
        serializer.is_valid(raise_exception=True)

        product_external_key = serializer.validated_data["product_external_key"]
        external_response = self.get_product_by_external_key(product_external_key)

        product_name = external_response["name"]

        with transaction.atomic():
            DefaultProductImage.objects.get_or_create(
                product_external_key=product_external_key,
                product_name=product_name,
            )

            item = serializer.save(product_name=product_name)

        response_serializer = WishlistItemSerializer(
            item, context={"request": request, "wishlist": wishlist}
        )

        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    def get_product_by_external_key(self, product_external_key):
        response = price_scrapper_client.get_product_by_id(product_external_key)

        if isinstance(response, ExternalServiceError):
            raise exceptions.APIException(
                detail=response.message, code=status.HTTP_502_BAD_GATEWAY
            )

        if response.status != 200:
            raise exceptions.APIException(
                detail="Failed to retrieve product information from external service.",
                code=status.HTTP_502_BAD_GATEWAY,
            )

        return response.data


class WhishlistItemDeleteView(BaseWishlistItemView):
    def delete(self, request, item_id):
        wishlist = self.get_wishlist(request)

        if not wishlist:
            return Response(
                {"detail": "Wishlist not found."}, status=status.HTTP_404_NOT_FOUND
            )

        try:
            item = WishlistItem.objects.get(id=item_id, wishlist=wishlist)
        except WishlistItem.DoesNotExist:
            return Response(
                {"detail": "Wishlist item not found."}, status=status.HTTP_404_NOT_FOUND
            )

        item.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
