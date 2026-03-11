"""
populate_db_v3.py — Standard Django Populate Script.

This version uses the standard Django ImageField.save() method.
When CLOUDINARY_URL is present, Django uses MediaCloudinaryStorage
to automatically handle the upload, folder pathing (media/products),
and URL generation.
"""

import os
import django
from pathlib import Path
from django.core.files import File

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'leafypop_project.settings')

# Load .env
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

django.setup()

from store.models import Product, SubscriptionPack, FAQ

# -- Path to local static images -----------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
STATIC_IMAGES_DIR = BASE_DIR / 'store' / 'static' / 'store' / 'images'

# -- Product data --------------------------------------------------------------
products_data = [
    {
        'name': 'Broccoli Microgreens',
        'price_50g': 125,
        'price_100g': 225,
        'image_file': 'brocallymicrogreen.png',
        'description': 'Highly nutritious and mild flavor.',
    },
    {
        'name': 'Beetroot Microgreens',
        'price_50g': 95,
        'price_100g': 170,
        'image_file': 'beetrootmicrogreen.png',
        'description': 'Vibrant red stems with a sweet, earthy flavor.',
    },
    {
        'name': 'Sunflower Microgreens',
        'price_50g': 70,
        'price_100g': 125,
        'image_file': 'sunflowermicrogreen.png',
        'description': 'Nutty, crunchy, and rich in protein.',
    },
    {
        'name': 'Pea Shoot Microgreens',
        'price_50g': 70,
        'price_100g': 125,
        'image_file': 'peasoot microgreen.png',
        'description': 'Sweet, crunchy shoots, perfect for salads.',
    },
    {
        'name': 'Radish Microgreens',
        'price_50g': 60,
        'price_100g': 110,
        'image_file': 'radish microgreen.png',
        'description': 'Spicy and peppery, adds a kick to any dish.',
    },
    {
        'name': 'Leafypop Mix Microgreens',
        'price_50g': 90,
        'price_100g': 160,
        'image_file': 'mix_microgreen.jpeg',
        'description': 'A healthy mix of our best microgreens.',
    },
]

# -- Populate Products ---------------------------------------------------------
print('')
print('== Populating Products (with Image Upload) ==')

# Clear existing products to ensure clean names and Cloudinary sync
Product.objects.all().delete()

for data in products_data:
    p, created = Product.objects.get_or_create(name=data['name'])
    p.price_50g = data['price_50g']
    p.price_100g = data['price_100g']
    p.description = data['description']

    local_path = STATIC_IMAGES_DIR / data['image_file']
    if local_path.exists():
        print(f"  Uploading {data['image_file']} for {p.name}...")
        with open(local_path, 'rb') as f:
            # save=True will commit to DB, Cloudinary storage will handle the upload
            p.image.save(data['image_file'], File(f), save=True)
    else:
        print(f"  [WARNING] Image {data['image_file']} not found locally.")
        p.save()
    
    status = 'Created' if created else 'Updated'
    print(f"  {status}: {p.name}")
    try:
        print(f"  -> URL: {p.image.url}")
    except:
        print("  -> URL: Error (check Cloudinary config)")

# -- End of populate script --
print('\n== Database population complete! ==')
