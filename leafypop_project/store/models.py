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

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0, help_text="Order in which FAQ appears")

    class Meta:
        verbose_name_plural = "FAQs"
        ordering = ['order']

    def __str__(self):
        return self.question
