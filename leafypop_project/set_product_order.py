"""
Sets the correct display order for all products as specified by the client.

Order:
1. LeafyPop Mix Microgreens
2. White Radish Microgreens
3. Pea Shoot Microgreens
4. Sunflower Microgreens
5. Beetroot Microgreens
6. Broccoli Microgreens
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'leafypop_project.settings')
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
django.setup()

from store.models import Product

# Desired order: keyword -> order number
order_map = [
    ('mix',        1),
    ('radish',     2),
    ('pea',        3),
    ('sunflower',  4),
    ('beetroot',   5),
    ('broccoli',   6),
]

print("Setting product display order...\n")
for keyword, order in order_map:
    qs = Product.objects.filter(name__icontains=keyword)
    if qs.exists():
        p = qs.first()
        p.display_order = order
        p.save(update_fields=['display_order'])
        print(f"  ✅ [{order}] {p.name}")
    else:
        print(f"  ⚠️  Not found: keyword='{keyword}'")

print("\n✅ Done. Current products in order:")
for p in Product.objects.order_by('display_order', 'id'):
    print(f"  {p.display_order}. {p.name}")
