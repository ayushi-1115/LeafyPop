import os
import django
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'leafypop_project.settings')

# Load .env
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

django.setup()

from store.models import Product

print("== DEBUG: Product Image URLs ==")
products = Product.objects.all()
if not products:
    print("No products found in DB!")
else:
    for p in products:
        try:
            print(f"Product: {p.name}")
            print(f"  - Value in DB: {p.image}")
            print(f"  - Generated URL: {p.image.url}")
        except Exception as e:
            print(f"  - Error getting URL: {e}")
print("===============================")
