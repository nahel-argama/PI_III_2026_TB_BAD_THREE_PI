from django.db import models
from django.conf import settings

class Producer(models.Model):

    class DocumentType(models.TextChoices):
        CPF = 'CPF', 'CPF'
        CNPJ = 'CNPJ', 'CNPJ'

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='producer',
        db_column='id_user'
    )

    document_type = models.CharField(
        max_length=4,
        choices=DocumentType.choices
    )

    document_number = models.CharField(
        max_length=20,
        unique=True,
        null=False,
        blank=False
    )

    trade_name = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    class Meta:
        db_table = 'producer'

    def __str__(self):
        return f"{self.trade_name or self.user.name} ({self.document_number})"