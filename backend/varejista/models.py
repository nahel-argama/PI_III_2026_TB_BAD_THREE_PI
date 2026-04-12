from django.db import models
from django.conf import settings

class Varejista(models.Model):

    class TipoDocumento(models.TextChoices):
        CPF = 'CPF', 'CPF'
        CNPJ = 'CNPJ', 'CNPJ'

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='varejista'
    )

    tipo_documento = models.CharField(
        max_length=4,
        choices=TipoDocumento.choices,
        null=False,
        blank=False
    )

    documento = models.CharField(
        max_length=20,
        unique=True,
        null=False,
        blank=False
    )

    def __str__(self):
        return f"{self.user.name} ({self.documento})"