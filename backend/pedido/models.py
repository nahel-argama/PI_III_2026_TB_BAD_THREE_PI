from django.db import models
from varejista.models import Varejista

class Pedido(models.Model):
    id = models.AutoField(primary_key=True, db_column='id_pedido')
    varejista = models.ForeignKey(to=Varejista, on_delete=models.CASCADE, db_column='id_varejista')

    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('CONFIRMADO', 'Confirmado'),
        ('CANCELADO', 'Cancelado'),
        ('ENTREGUE', 'Entregue')
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDENTE')
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido {self.id_pedido} - Varejista: {self.id_varejista.nome} - Status: {self.status}"