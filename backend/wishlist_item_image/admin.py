from django.contrib import admin
from .models import WishlistItemImage


@admin.register(WishlistItemImage)
class WishlistItemImageAdmin(admin.ModelAdmin):
    list_display = ("id", "product_external_key", "image")
    search_fields = ("product_external_key",)
