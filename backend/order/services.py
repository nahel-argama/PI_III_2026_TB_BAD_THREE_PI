from django.db import transaction
from django.db.models import F

from product.models import Product


def validate_item_stock(product, quantity):
    if not product.is_active:
        return f"Product {product.id} is not available"

    if quantity > product.available_quantity:
        return (
            f"Product {product.id} has only "
            f"{product.available_quantity:g} units available"
        )

    return None


def confirm_order_with_stock(order):
    with transaction.atomic():
        order = (
            order.__class__.objects
            .select_for_update()
            .prefetch_related('items')
            .get(pk=order.pk)
        )

        if order.status != 'PENDING':
            return order, f"Order status is {order.status}, not PENDING"

        items = list(order.items.select_related('product'))
        if not items:
            return order, "Cannot confirm order with no items"

        product_ids = [item.product_id for item in items]
        products = Product.objects.select_for_update().in_bulk(product_ids)

        for item in items:
            product = products[item.product_id]
            error = validate_item_stock(product, item.quantity)
            if error:
                return order, error

        for item in items:
            Product.objects.filter(pk=item.product_id).update(
                total_quantity=F('total_quantity') - item.quantity
            )

        order.status = 'CONFIRMED'
        order.save(update_fields=['status'])

    return order, None
