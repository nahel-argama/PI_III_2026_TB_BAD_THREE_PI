import os
import requests
from requests.exceptions import RequestException

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


def process_payment_and_confirm(order, payment_method, price, card=None):
    gateway_url = os.environ.get('PAYMENT_GATEWAY_URL', 'http://localhost:8002')
    url = f"{gateway_url}/payments"

    payload = {
        "price": float(price),
        "payment_method": payment_method
    }

    if payment_method == 'credit_card' and card:
        payload["card"] = card

    try:
        response = requests.post(url, json=payload, timeout=10)

        if response.status_code in (402, 422):
            order.status = 'CANCELED'
            order.save(update_fields=['status'])

            try:
                data = response.json()
            except ValueError:
                data = {}

            error_msg = data.get("message")
            if not error_msg:
                detail = data.get("detail")
                if isinstance(detail, dict):
                    error_msg = detail.get("message")
                elif isinstance(detail, str):
                    error_msg = detail

            if not error_msg:
                error_msg = "Pagamento recusado pelo gateway."

            errors = data.get("errors") if isinstance(data.get("errors"), list) else []

            return None, {"status": response.status_code, "error": error_msg, "gateway_errors": errors}

        response.raise_for_status()

        # Sucesso no gateway, confirma pedido e baixa estoque
        order, error = confirm_order_with_stock(order)
        if error:
            return None, {"status": 400, "error": error}

        return order, None

    except RequestException:
        return None, {"status": 503, "error": "Serviço de pagamento indisponível. Tente novamente."}
