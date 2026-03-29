from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

# Product Model: Defines the structure for microgreen products in the database
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price_50g = models.DecimalField(max_digits=6, decimal_places=2, default=0.00, verbose_name="Price (50g)")
    price_100g = models.DecimalField(max_digits=6, decimal_places=2, default=0.00, verbose_name="Price (100g)")
    is_in_stock = models.BooleanField(default=True)
    image = models.ImageField(upload_to='products/')
    display_order = models.PositiveIntegerField(default=0, help_text="Set the display order on the homepage (1 = first)")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['display_order', 'id']

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

# Review Model: Customer testimonials/reviews
class Review(models.Model):
    RATING_CHOICES = [(i, '⭐' * i) for i in range(1, 6)]  # 1 to 5 stars
    
    customer_name = models.CharField(max_length=100)
    rating = models.IntegerField(choices=RATING_CHOICES, default=5)
    review_text = models.TextField(max_length=500)
    image = models.ImageField(upload_to='reviews/', null=True, blank=True)
    is_approved = models.BooleanField(default=False, help_text="Admin must approve before showing on site")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.customer_name} - {'⭐' * self.rating}"

# --- SIGNALS FOR AUTO-NOTIFICATIONS ---
@receiver(post_save, sender=UserActivity)
def send_activity_notification(sender, instance, created, **kwargs):
    """
    Automatically sends an email to the admin whenever a new activity is logged.
    This ensures the client stays informed about all site interactions.
    """
    if created:
        admin_emails = ['leafypop.eco@gmail.com']
        subject = f"🔔 Site Activity: {instance.activity_type}"
        message = (
            f"Movement detected on LeafyPop:\n\n"
            f"User: {instance.user.username}\n"
            f"Action: {instance.activity_type}\n"
            f"Details: {instance.details or 'None'}\n"
            f"Time: {instance.timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n"
        )
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                admin_emails,
                fail_silently=True
            )
        except Exception as e:
            # Silent fail to prevent user-facing errors if email config is missing
            print(f"Admin Notification Error: {e}")
