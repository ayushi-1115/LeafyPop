from django.contrib import admin
from .models import Product

from django.utils.html import format_html

# Custom Admin Site Configuration
admin.site.site_header = "LeafyPop Administration"
admin.site.site_title = "LeafyPop Admin Portal"
admin.site.index_title = "Welcome to LeafyPop Manager"

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_in_stock', 'created_at', 'image_preview')
    list_editable = ('price', 'is_in_stock')
    search_fields = ('name',)
    list_filter = ('is_in_stock', 'created_at')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: auto;" />', obj.image.url)
        return ""
    image_preview.short_description = 'Image'

admin.site.register(Product, ProductAdmin)
