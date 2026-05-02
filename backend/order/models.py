from django.db import models
from retailer.models import Retailer

class Order(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='id_order')
    retailer = models.ForeignKey(to=Retailer, on_delete=models.CASCADE, db_column='id_retailer')

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELED', 'Canceled'),
        ('DELIVERED', 'Delivered')
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    total_value = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')

    class Meta:
        db_table = 'order'

    def __str__(self):
        return f"Order {self.id} - Retailer: {self.retailer.user.name} - Status: {self.status}"