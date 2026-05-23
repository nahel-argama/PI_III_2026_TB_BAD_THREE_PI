from django.db import models
from retailer.models import Retailer
from producer.models import Producer

class Order(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='id_order')
    retailer = models.ForeignKey(to=Retailer, on_delete=models.CASCADE, db_column='id_retailer')
    producer = models.ForeignKey(
        to=Producer,
        on_delete=models.CASCADE,
        db_column='id_producer',
        related_name='orders'
    )

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELED', 'Canceled'),
        ('DELIVERED', 'Delivered')
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    subtotal_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fee_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')

    class Meta:
        db_table = 'order'
        constraints = [
            models.UniqueConstraint(
                fields=['retailer', 'producer'],
                condition=models.Q(status='PENDING'),
                name='unique_pending_order_per_retailer_producer'
            )
        ]

    def __str__(self):
        return f"Order {self.id} - Retailer: {self.retailer.user.name} - Producer: {self.producer.user.name} - Status: {self.status}"
