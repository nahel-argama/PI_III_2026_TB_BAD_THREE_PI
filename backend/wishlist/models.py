from django.db import models
from retailer.models import Retailer


class Wishlist(models.Model):
    id = models.BigAutoField(primary_key=True, db_column="id_wishlist")
    retailer = models.OneToOneField(
        Retailer,
        on_delete=models.CASCADE,
        related_name="wishlist",
        db_column="id_retailer",
    )

    class Meta:
        db_table = "wishlist"

    def __str__(self):
        return f"Wishlist {self.id} - {self.retailer.user.name}"
