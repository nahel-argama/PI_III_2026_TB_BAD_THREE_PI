from django.db import models
from image.models import Image


class WishlistItemImage(models.Model):
    id = models.BigAutoField(primary_key=True, db_column="id_wishlist_item_image")
    product_external_key = models.TextField(unique=True)
    image = models.ForeignKey(
        Image,
        on_delete=models.CASCADE,
        related_name="wishlist_item_images",
        db_column="id_image",
    )

    class Meta:
        db_table = "wishlist_item_image"

    def __str__(self):
        return f"WishlistItemImage {self.id} - {self.product_external_key}"
