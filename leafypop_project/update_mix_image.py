import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'leafypop_project.settings')
django.setup()

from store.models import Product

try:
    p = Product.objects.get(name='Leafypop Mix Microgreens')
    p.image = 'products/mix_microgreen.jpeg'
    p.save()
    print("Successfully updated Leafypop Mix image path.")
except Product.DoesNotExist:
    print("Product 'Leafypop Mix Microgreens' not found.")
