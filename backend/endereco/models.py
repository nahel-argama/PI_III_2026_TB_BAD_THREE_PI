from django.db import models
from django.conf import settings
from estado.models import Estado 

class Endereco(models.Model):
    id_endereco = models.AutoField(primary_key=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='enderecos'
    )

    rua = models.CharField(max_length=150)
    numero = models.CharField(max_length=10, null=True, blank=True)
    bairro = models.CharField(max_length=100, null=True, blank=True)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    cep = models.CharField(max_length=10)

    estado = models.ForeignKey(
        Estado,
        on_delete=models.PROTECT,
        related_name='enderecos'
    )

    def __str__(self):
        return f"{self.rua}, {self.numero} - {self.cidade}/{self.estado.sigla}"