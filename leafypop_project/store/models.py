from django.db import models

# Product Model: Defines the structure for microgreen products in the database
class Product(models.Model):
    name = models.CharField(max_length=100) # Name of the product (e.g., Broccoli Microgreens)
    description = models.TextField() # Detailed description of the product
    # Price fields for different quantities
    price_50g = models.DecimalField(max_digits=6, decimal_places=2, default=0.00, verbose_name="Price (50g)")
    price_100g = models.DecimalField(max_digits=6, decimal_places=2, default=0.00, verbose_name="Price (100g)")
    is_in_stock = models.BooleanField(default=True) # Checkbox to show/hide if product is available
    image = models.ImageField(upload_to='products/') # Image file stored in media/products/
    created_at = models.DateTimeField(auto_now_add=True) # Automatically set date when created

    def __str__(self):
        return self.name

# SubscriptionPack Model: Defines predefined bundles/plans
class SubscriptionPack(models.Model):
    name = models.CharField(max_length=100) # Trial Pack, Family Pack, etc.
    description = models.TextField() # e.g., "3 varieties x 50 gm"
    one_time_price = models.DecimalField(max_digits=6, decimal_places=2)
    monthly_plan_price = models.DecimalField(max_digits=6, decimal_places=2)
    
    def __str__(self):
        return self.name

# FAQ Model: Stores Frequently Asked Questions shown on the home page
class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0, help_text="Order in which FAQ appears") # For manual sorting

    class Meta:
        verbose_name_plural = "FAQs" # Correct plural naming in Admin panel
        ordering = ['order'] # Sort by the 'order' field by default

    def __str__(self):
        return self.question

# UserActivity Model: Tracks login logs for the Master Dashboard
from django.contrib.auth.models import User

class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=50, default="Login") # e.g., Login, View Dashboard
    details = models.TextField(blank=True, null=True) # Extra info like "Added Product X"
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "User Activities"
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user.username} - {self.activity_type} at {self.timestamp}"
