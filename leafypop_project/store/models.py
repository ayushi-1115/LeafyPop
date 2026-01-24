from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price_50g = models.DecimalField(max_digits=6, decimal_places=2, default=0.00, verbose_name="Price (50g)")
    price_100g = models.DecimalField(max_digits=6, decimal_places=2, default=0.00, verbose_name="Price (100g)")
    is_in_stock = models.BooleanField(default=True)
    image = models.ImageField(upload_to='products/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class SubscriptionPack(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    one_time_price = models.DecimalField(max_digits=6, decimal_places=2)
    monthly_plan_price = models.DecimalField(max_digits=6, decimal_places=2)
    
    def __str__(self):
        return self.name
