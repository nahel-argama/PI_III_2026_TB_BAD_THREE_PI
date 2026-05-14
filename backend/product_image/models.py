from django.db import models

from image.models import Image
from product.models import Product


class ProductImage(models.Model):
    id = models.BigAutoField(primary_key=True, db_column="id_product_image")
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
        db_column="id_product",
    )
    image = models.ForeignKey(
        Image,
        on_delete=models.CASCADE,
        related_name="product_images",
        db_column="id_image",
    )
    created_at = models.DateTimeField(auto_now_add=True, db_column="created_at")

    class Meta:
        db_table = "product_image"

    def __str__(self):
        return f"ProductImage {self.id} for product {self.product_id}"
