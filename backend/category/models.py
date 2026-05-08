from django.db import models


class Category(models.Model):
    id = models.AutoField(primary_key=True, db_column='id_category')

    name = models.CharField(
        max_length=100,
        unique=True
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'category'

    def __str__(self):
        return self.name