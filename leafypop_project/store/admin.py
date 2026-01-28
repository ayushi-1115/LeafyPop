from django.contrib import admin
from .models import Product, SubscriptionPack, FAQ
from django.utils.html import format_html

# Custom Admin Site Configuration: Changes the branding of the Django Admin
admin.site.site_header = "LeafyPop Administration"
admin.site.site_title = "LeafyPop Admin Portal"
admin.site.index_title = "Welcome to LeafyPop Manager"

# ProductAdmin: Customizes how Products look in the Admin panel
class ProductAdmin(admin.ModelAdmin):
    # Columns to show in the list view
    list_display = ('name', 'price_50g', 'price_100g', 'is_in_stock', 'created_at', 'image_preview')
    # Allows editing these fields directly from the list view (no need to click into the product)
    list_editable = ('price_50g', 'price_100g', 'is_in_stock')
    search_fields = ('name',) # Adds a search bar for names
    list_filter = ('is_in_stock', 'created_at') # Adds filtering options on the right sidebar

    # Shows a tiny image of the product in the admin list
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: auto;" />', obj.image.url)
        return ""
    image_preview.short_description = 'Image'

# Register SubscriptionPack with basic list editing
@admin.register(SubscriptionPack)
class SubscriptionPackAdmin(admin.ModelAdmin):
    list_display = ('name', 'one_time_price', 'monthly_plan_price')
    list_editable = ('one_time_price', 'monthly_plan_price')

# Register FAQ with manual sorting
@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'order')
    list_editable = ('order',)

# Link the Product model to its custom Admin configuration
admin.site.register(Product, ProductAdmin)

from .models import UserActivity
@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity_type', 'timestamp', 'ip_address')
    list_filter = ('activity_type', 'timestamp')
    search_fields = ('user__username', 'activity_type')
