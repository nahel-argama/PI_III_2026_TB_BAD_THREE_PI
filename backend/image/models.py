from django.db import models


class Image(models.Model):
    id = models.BigAutoField(primary_key=True, db_column="id_image")
    url = models.TextField(db_column="url")
    created_at = models.DateTimeField(auto_now_add=True, db_column="created_at")

    class Meta:
        db_table = "image"

    def __str__(self):
        return self.url
