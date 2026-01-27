import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'leafypop_project.settings')
django.setup()

from store.models import Product

mapping = {
    'Beetroot Microgreens': 'products/beetrootmicrogreen.png',
    'Broccoli Microgreens': 'products/brocallymicrogreen.png',
    'Pea Shoot Microgreens': 'products/peasoot microgreen.png',
    'Radish Microgreens': 'products/radish microgreen.png',
    'Sunflower Microgreens': 'products/sunflowermicrogreen.png'
}

for name, img_path in mapping.items():
    p, created = Product.objects.get_or_create(name=name)
    p.image = img_path
    if not p.description:
        p.description = "Fresh and natural microgreens."
    p.save()
    print(f"{'Created' if created else 'Updated'} {name} with {img_path}")
