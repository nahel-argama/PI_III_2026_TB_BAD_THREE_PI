from django.db import models
from wishlist.models import Wishlist


class WishlistItem(models.Model):
    id = models.BigAutoField(primary_key=True, db_column="id_wishlist_item")
    wishlist = models.ForeignKey(
        Wishlist,
        on_delete=models.CASCADE,
        related_name="items",
        db_column="id_wishlist",
    )
    product_external_key = models.BigIntegerField(null=False, unique=True)
    product_name = models.CharField(max_length=255, null=False, blank=False)

    class Meta:
        db_table = "wishlist_item"

    def __str__(self):
        return f"{self.product_name} ({self.product_external_key})"
