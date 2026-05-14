from django.db import models

from image.models import Image


class DefaultProductImage(models.Model):
    id = models.BigAutoField(
        primary_key=True, db_column="id_default_product_image"
    )
    product_external_key = models.TextField(
        unique=True, db_column="product_external_key"
    )
    product_name = models.CharField(
        max_length=150, db_column="product_name", blank=True
    )
    image = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        related_name="default_product_images",
        db_column="id_image",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, db_column="created_at")

    class Meta:
        db_table = "default_product_image"
        indexes = [models.Index(fields=["product_external_key"])]

    def __str__(self):
        return f"DefaultProductImage {self.product_external_key}"
