from django.contrib import admin
from .models import Product, SubscriptionPack, FAQ
from django.utils.html import format_html

# Custom Admin Site Configuration
admin.site.site_header = "LeafyPop Administration"
admin.site.site_title = "LeafyPop Admin Portal"
admin.site.index_title = "Welcome to LeafyPop Manager"

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_50g', 'price_100g', 'is_in_stock', 'created_at', 'image_preview')
    list_editable = ('price_50g', 'price_100g', 'is_in_stock')
    search_fields = ('name',)
    list_filter = ('is_in_stock', 'created_at')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: auto;" />', obj.image.url)
        return ""
    image_preview.short_description = 'Image'

@admin.register(SubscriptionPack)
class SubscriptionPackAdmin(admin.ModelAdmin):
    list_display = ('name', 'one_time_price', 'monthly_plan_price')
    list_editable = ('one_time_price', 'monthly_plan_price')

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'order')
    list_editable = ('order',)

admin.site.register(Product, ProductAdmin)
