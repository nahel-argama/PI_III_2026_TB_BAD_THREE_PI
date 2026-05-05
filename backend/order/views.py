from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction
from .serializers import OrderSerializer
from order_item.serializers import OrderItemSerializer
from users.permissions import IsRetailer
from .filters import OrderFilter
from .models import Order
from order_item.models import OrderItem
from product.models import Product


class OrderViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter

    def get_permissions(self):
        if self.action in ['create', 'add_item']:
            return [IsAuthenticated(), IsRetailer()]

        if self.action in ['update', 'partial_update', 'confirm']:
            return [IsAuthenticated(), IsRetailer()]

        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user

        if user.user_type == 'RETAILER':
            return Order.objects.filter(retailer=user.retailer).prefetch_related('items')

        if user.user_type == 'PRODUCER':
            return Order.objects.filter(
                producer=user.producer
            ).prefetch_related('items').distinct()

        return Order.objects.none()

    def perform_create(self, serializer):
        serializer.save(retailer=self.request.user.retailer)

    @action(detail=False, methods=['post'])
    def add_item(self, request):
        """
        Add an item to an order (create or get existing order)
        
        POST /api/orders/add_item/
        {
            "product_id": 1,
            "quantity": 5
        }
        """
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')

        # Validations
        if not product_id or quantity is None:
            return Response(
                {"error": "product_id and quantity are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Convert quantity to int and validate
        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError()
        except (ValueError, TypeError):
            return Response(
                {"error": "quantity must be a positive integer"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if not product.is_active:
            return Response(
                {"error": "Product is not available"},
                status=status.HTTP_400_BAD_REQUEST
            )

        retailer = request.user.retailer

        # Check if there's an open order for this retailer + producer
        try:
            with transaction.atomic():
                order, created = Order.objects.get_or_create(
                    retailer=retailer,
                    producer=product.producer,
                    status='PENDING',
                    defaults={'total_value': 0}
                )

                # Check if product already exists in order
                order_item, item_created = OrderItem.objects.get_or_create(
                    order=order,
                    product=product,
                    defaults={
                        'quantity': quantity,
                        'unit_price': product.price
                    }
                )

                # If item already exists, update quantity
                if not item_created:
                    order_item.quantity += quantity
                    order_item.save()

                serializer = OrderSerializer(order)
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
                )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        """
        Confirm/close an order (change status to CONFIRMED)
        
        POST /api/orders/<id>/confirm/
        """
        order = self.get_object()

        if order.status != 'PENDING':
            return Response(
                {"error": f"Order status is {order.status}, not PENDING"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not order.items.exists():
            return Response(
                {"error": "Cannot confirm order with no items"},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status = 'CONFIRMED'
        order.save()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """
        Cancel an order (change status to CANCELED)
        
        POST /api/orders/<id>/cancel/
        """
        order = self.get_object()

        if order.status in ['CANCELED', 'DELIVERED']:
            return Response(
                {"error": f"Cannot cancel order with status {order.status}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status = 'CANCELED'
        order.save()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def items(self, request, pk=None):
        """Get items from an order"""
        order = self.get_object()
        user = request.user

        if user.user_type == 'RETAILER':
            items = order.items.all()

        elif user.user_type == 'PRODUCER':
            items = order.items.filter(
                product__producer=user.producer
            )

        else:
            items = []

        serializer = OrderItemSerializer(items, many=True)
        return Response(serializer.data)