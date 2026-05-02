from django.db import models
from order.models import Order
from product.models import Product
from producer.models import Producer
from retailer.models import Retailer
from django.core.validators import MinValueValidator, MaxValueValidator

class Review(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='id_review')
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, db_column='id_order')
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, db_column='id_product')
    producer = models.ForeignKey(to=Producer, on_delete=models.CASCADE, db_column='id_producer')
    retailer = models.ForeignKey(to=Retailer, on_delete=models.CASCADE, db_column='id_retailer')
    rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')

    class Meta:
        db_table = 'review'

    def __str__(self):
        return f"Review {self.id} - Order: {self.order.id} - Product: {self.product.name} - Producer: {self.producer.user.name} - Retailer: {self.retailer.user.name} - Rating: {self.rating}"