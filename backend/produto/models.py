from django.db import models
from produtor.models import Produtor
from categoria.models import Categoria

class Produto(models.Model):
    
    id_produto = models.AutoField(primary_key=True, null=False)

    id_categoria = models.ForeignKey(
        to=Categoria, 
        on_delete=models.CASCADE, 
        related_name='produtos', 
        null=False
    )

    id_produtor = models.ForeignKey(
        to=Produtor,
        on_delete=models.CASCADE,
        related_name='produtos',
        null=False
    )

    nome = models.CharField(max_length=150, blank=False, null=False)

    descricao = models.TextField(
        null=True,
        blank=True
    )

    quantidade_total = models.FloatField(null=False)

    quantidade_reservada = models.FloatField(null=False)

    preco = models.DecimalField(max_digits=10, decimal_places=2)

    ativo = models.BooleanField(default=True)

    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome