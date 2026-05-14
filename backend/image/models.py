from django.db import models


class Image(models.Model):
    id = models.BigAutoField(primary_key=True, db_column="id_image")
    blob = models.BinaryField(db_column="blob")
    mime_type = models.CharField(max_length=100, db_column="mime_type")
    created_at = models.DateTimeField(auto_now_add=True, db_column="created_at")

    class Meta:
        db_table = "image"

    def __str__(self):
        return f"Image {self.id} ({self.mime_type})"
