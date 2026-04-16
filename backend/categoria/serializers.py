from rest_framework import serializers
from .models import Categoria


class CategoriaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categoria
        fields = [
            'id_categoria',
            'nome',
            'ativo'
        ]

    def validate_nome(self, value):
        return value.strip().title()