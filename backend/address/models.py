from django.db import models
from django.conf import settings


class Address(models.Model):
    id = models.BigAutoField(primary_key=True, db_column="id_address")

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="address",
        db_column="id_user",
    )

    street = models.CharField(max_length=150, db_column="street")
    number = models.CharField(max_length=10)
    complement = models.TextField(blank=True)
    neighborhood = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    postal_code = models.CharField(max_length=10)
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        db_index=True,
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        db_index=True,
    )

    class Meta:
        db_table = "address"

    def __str__(self):
        return f"{self.street}, {self.number} - {self.city}/{self.state}"
