from django.db import models
from producer.models import Producer
from category.models import Category

class Product(models.Model):

    id = models.BigAutoField(primary_key=True, null=False, db_column='id_product')

    category = models.ForeignKey(
        to=Category,
        on_delete=models.CASCADE,
        related_name='products',
        db_column='id_category',
        null=False
    )

    producer = models.ForeignKey(
        to=Producer,
        on_delete=models.CASCADE,
        related_name='products',
        db_column='id_producer',
        null=False
    )

    name = models.CharField(max_length=150, blank=False, null=False)

    description = models.TextField(
        null=True,
        blank=True
    )

    total_quantity = models.FloatField(null=False)

    reserved_quantity = models.FloatField(null=False)

    price = models.DecimalField(max_digits=10, decimal_places=2)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')

    class Meta:
        db_table = 'product'

    def __str__(self):
        return self.name