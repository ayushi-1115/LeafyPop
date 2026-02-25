"""
populate_db_v3.py — Cloudinary-aware populate script.

This script:
1. Opens each product image from the local static files directory
2. Uploads it directly to Cloudinary using the SDK
3. Saves the returned Cloudinary URL into the Product.image field

This fixes the problem where populate_db_v2.py only stored a local path
string (e.g. 'products/brocallymicrogreen.png') which broke after the
Render database reset, because Django's ImageField.url then pointed to
a missing /media/ path instead of a real Cloudinary URL.

Run: python populate_db_v3.py
"""

import os
import django
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'leafypop_project.settings')

# Load .env BEFORE django.setup() so env vars are available
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

django.setup()

import cloudinary
import cloudinary.uploader

# Explicitly configure Cloudinary from the CLOUDINARY_URL env var.
# django-cloudinary-storage reads this automatically, but the raw
# cloudinary SDK needs an explicit config() call when running outside
# a full web server context (e.g. in a populate script).
cloudinary_url = os.environ.get('CLOUDINARY_URL')
if cloudinary_url:
    cloudinary.config(cloudinary_url=cloudinary_url)
    print('Cloudinary configured OK.')
else:
    print('[ERROR] CLOUDINARY_URL not found in environment. Check your .env file.')
    exit(1)

from store.models import Product, SubscriptionPack, FAQ

# ── Path to local static images ─────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent
STATIC_IMAGES_DIR = BASE_DIR / 'store' / 'static' / 'store' / 'images'

# ── Product data ─────────────────────────────────────────────────────────────
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
        'image_file': 'peasoot microgreen.png',   # note: space in filename
        'description': 'Sweet, crunchy shoots, perfect for salads.',
    },
    {
        'name': 'Radish Microgreens',
        'price_50g': 60,
        'price_100g': 110,
        'image_file': 'radish microgreen.png',    # note: space in filename
        'description': 'Spicy and peppery, adds a kick to any dish.',
    },
    {
        'name': 'Leafypop Mix Microgreens',
        'price_50g': 90,
        'price_100g': 160,
        # mix_microgreen.jpeg is missing locally — using leafypopp.jpeg instead
        'image_file': 'leafypopp.jpeg',
        'description': 'A healthy mix of our best microgreens.',
    },
]

# ── Subscription packs ───────────────────────────────────────────────────────
subscriptions_data = [
    {
        'name': 'Trial Pack',
        'one_time_price': 230,
        'monthly_plan_price': 880,
        'description': '3 varieties × 50 gm',
    },
    {
        'name': 'Regular Family Pack',
        'one_time_price': 420,
        'monthly_plan_price': 1599,
        'description': '3 varieties × 100 gm',
    },
]

# ── FAQs ─────────────────────────────────────────────────────────────────────
faqs_data = [
    {
        'question': 'What are microgreens?',
        'answer': 'Microgreens are young vegetable greens that are approximately 1–3 inches tall. '
                  'They are harvested just after the first true leaves have developed.',
        'order': 1,
    },
    {
        'question': 'Are your microgreens organic?',
        'answer': 'Yes! All our microgreens are 100% pesticide-free and grown using clean, '
                  'soil-less methods with filtered water.',
        'order': 2,
    },
    {
        'question': 'How do I store microgreens?',
        'answer': 'Store them in the refrigerator in an airtight container. They stay fresh for '
                  '5–7 days. Do not wash until just before use.',
        'order': 3,
    },
    {
        'question': 'How do I place an order?',
        'answer': 'Click "Order Now" on any product and you will be redirected to WhatsApp to '
                  'complete your order with our support team.',
        'order': 4,
    },
]

# ── Helper: upload to Cloudinary ─────────────────────────────────────────────
def upload_image_to_cloudinary(filename, folder='products'):
    """Upload a local image file to Cloudinary and return the public_id."""
    local_path = STATIC_IMAGES_DIR / filename
    if not local_path.exists():
        print('  [WARNING] Image file not found: ' + str(local_path))
        return None
    print('  Uploading ' + filename + ' to Cloudinary...')
    result = cloudinary.uploader.upload(
        str(local_path),
        folder=folder,
        # Use filename (without extension) as public_id so re-runs are idempotent
        public_id=Path(filename).stem.replace(' ', '_'),
        overwrite=True,
        resource_type='image',
    )
    url = result.get('secure_url')
    print('[OK] Uploaded -> ' + url)
    return result.get('public_id')   # Return public_id so Django ImageField stores it correctly

# -- Populate Products ---------------------------------------------------------
print('')
print('== Populating Products ==')
for data in products_data:
    p, created = Product.objects.get_or_create(name=data['name'])
    p.price_50g = data['price_50g']
    p.price_100g = data['price_100g']

    if not data.get('description', '').strip() == 'Fresh and natural microgreens.':
        p.description = data['description']

    # Always re-upload image so we always have a valid Cloudinary URL,
    # even after a database wipe.
    public_id = upload_image_to_cloudinary(data['image_file'], folder='products')
    if public_id:
        p.image = public_id   # Django cloudinary_storage uses public_id

    p.save()
    status = 'Created' if created else 'Updated'
    print('  ' + status + ': ' + data['name'])

# -- Populate Subscription Packs -----------------------------------------------
print('')
print('== Populating Subscription Packs ==')
for data in subscriptions_data:
    s, created = SubscriptionPack.objects.get_or_create(name=data['name'])
    s.one_time_price = data['one_time_price']
    s.monthly_plan_price = data['monthly_plan_price']
    s.description = data['description']
    s.save()
    status = 'Created' if created else 'Updated'
    print('  ' + status + ': ' + data['name'])

# -- Populate FAQs (only if none exist) ----------------------------------------
print('')
print('== Populating FAQs ==')
for data in faqs_data:
    faq, created = FAQ.objects.get_or_create(question=data['question'])
    if created:
        faq.answer = data['answer']
        faq.order = data['order']
        faq.save()
        print('  Created FAQ: ' + data['question'])
    else:
        print('  Already exists: ' + data['question'])

print('')
print('== Database population complete! ==')

