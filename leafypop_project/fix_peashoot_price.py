import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'leafypop_project.settings')
django.setup()

from store.models import Product

# Correcting the price for Pea Shoot Microgreens
try:
    # Try multiple common name variations just to be safe
    p = Product.objects.filter(name__icontains='Pea').first()
    if p:
        p.price_50g = 70.00
        p.price_100g = 125.00
        p.save()
        print(f"Successfully updated prices for: {p.name}")
    else:
        print("Product containing 'Pea' not found.")
except Exception as e:
    print(f"Error: {e}")
