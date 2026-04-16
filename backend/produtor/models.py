from django.db import models
from django.conf import settings

class Produtor(models.Model):

    class TipoDocumento(models.TextChoices):
        CPF = 'CPF', 'CPF'
        CNPJ = 'CNPJ', 'CNPJ'

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True, 
        related_name='produtor'
    )

    tipo_documento = models.CharField(
        max_length=4,
        choices=TipoDocumento.choices
    )

    documento = models.CharField(
        max_length=20,
        unique=True,
        null=False,
        blank=False
    )

    nome_fantasia = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.nome_fantasia or self.user.name} ({self.documento})"