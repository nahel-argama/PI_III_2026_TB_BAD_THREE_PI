from django.db import models


class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)

    nome = models.CharField(
        max_length=100,
        unique=True
    )

    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome