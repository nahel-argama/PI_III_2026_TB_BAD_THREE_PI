from django.db import models
from django.db.models import Sum, F
from order.models import Order

def update_total(order):
    total = order.items.aggregate(
        total=Sum(F('quantity') * F('unit_price'))
    )['total'] or 0

    order.total_value = total
    order.save()

class OrderItem(models.Model):
    id = models.BigAutoField(primary_key=True, db_column="id_order_item")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', db_column='id_order')
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'order_item'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        update_total(self.order)

    def delete(self, *args, **kwargs):
        order = self.order
        super().delete(*args, **kwargs)
        update_total(order)