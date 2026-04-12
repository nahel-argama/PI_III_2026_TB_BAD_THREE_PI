from django.db import models
from produtor.models import Produtor

class Produto(models.Model):
    
    id_produto = models.AutoField(primary_key=True)

    produtor = models.ForeignKey(
        Produtor,
        on_delete=models.CASCADE,
        related_name='produtos'
    )

    nome = models.CharField(max_length=150)

    descricao = models.TextField(
        null=True,
        blank=True
    )

    preco = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    estoque = models.PositiveIntegerField()

    ativo = models.BooleanField(default=True)

    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome