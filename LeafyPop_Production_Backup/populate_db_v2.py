import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'leafypop_project.settings')
django.setup()

from store.models import Product, SubscriptionPack

# Product Data from PDF
products_data = [
    {
        'name': 'Broccoli Microgreens',
        'price_50g': 125,
        'price_100g': 225,
        'image': 'products/brocallymicrogreen.png',
        'description': 'Highly nutritious and mild flavor.'
    },
    {
        'name': 'Beetroot Microgreens',
        'price_50g': 95,
        'price_100g': 170,
        'image': 'products/beetrootmicrogreen.png',
        'description': 'Vibrant red stems with a sweet, earthy flavor.'
    },
    {
        'name': 'Sunflower Microgreens',
        'price_50g': 70,
        'price_100g': 125,
        'image': 'products/sunflowermicrogreen.png',
        'description': 'Nutty, crunchy, and rich in protein.'
    },
    {
        'name': 'Pea shoots Microgreens',
        'price_50g': 70,
        'price_100g': 125,
        'image': 'products/peasoot microgreen.png',
        'description': 'Sweet, crunchy shoots, perfect for salads.'
    },
    {
        'name': 'Radish Microgreens',
        'price_50g': 60,
        'price_100g': 110,
        'image': 'products/radish microgreen.png',
        'description': 'Spicy and peppery, adds a kick to any dish.'
    },
    {
        'name': 'Leafypop Mix Microgreens',
        'price_50g': 90,
        'price_100g': 160,
        'image': 'products/leafyypopp.png',
        'description': 'A healthy mix of our best microgreens.'
    },
]

# Subscription Packs Data from PDF
subscriptions_data = [
    {
        'name': 'Trial Pack',
        'one_time_price': 230,
        'monthly_plan_price': 880,
        'description': '3 varieties × 50 gm'
    },
    {
        'name': 'Regular Family Pack',
        'one_time_price': 420,
        'monthly_plan_price': 1599,
        'description': '3 varieties × 100 gm'
    },
]

# Populate Products
for data in products_data:
    p, created = Product.objects.get_or_create(name=data['name'])
    p.price_50g = data['price_50g']
    p.price_100g = data['price_100g']
    p.image = data['image']
    if not p.description or p.description == "Fresh and natural microgreens.":
        p.description = data['description']
    p.save()
    print(f"{'Created' if created else 'Updated'} Product: {data['name']}")

# Populate Subscriptions
for data in subscriptions_data:
    s, created = SubscriptionPack.objects.get_or_create(
        name=data['name'],
        defaults={
            'one_time_price': data['one_time_price'],
            'monthly_plan_price': data['monthly_plan_price'],
            'description': data['description']
        }
    )
    if not created:
        s.one_time_price = data['one_time_price']
        s.monthly_plan_price = data['monthly_plan_price']
        s.description = data['description']
        s.save()
    print(f"{'Created' if created else 'Updated'} Subscription: {data['name']}")

print("Database population complete!")
