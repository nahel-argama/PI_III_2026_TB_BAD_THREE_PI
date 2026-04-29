from django.db import models
from pedido.models import Pedido
from produto.models import Produto
from produtor.models import Produtor
from varejista.models import Varejista
from django.core.validators import MinValueValidator, MaxValueValidator

class Avaliacao(models.Model):
    id_avaliacao = models.AutoField(primary_key=True)
    id_pedido = models.ForeignKey(to=Pedido, on_delete=models.CASCADE)
    id_produto = models.ForeignKey(to=Produto, on_delete=models.CASCADE)
    id_produtor = models.ForeignKey(to=Produtor, on_delete=models.CASCADE)
    id_varejista = models.ForeignKey(to=Varejista, on_delete=models.CASCADE)
    nota = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    comentario = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Avaliação {self.id_avaliacao} - Pedido: {self.id_pedido.id_pedido} - Produto: {self.id_produto.nome} - Produtor: {self.id_produtor.nome} - Varejista: {self.id_varejista.nome} - Nota: {self.nota}"