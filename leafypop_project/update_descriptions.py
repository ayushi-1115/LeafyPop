import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'leafypop_project.settings')

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

django.setup()

from store.models import Product

# New detailed descriptions provided by client
descriptions = {
    'Beetroot Microgreens': 'Vibrant and slightly earthy in flavor, beetroot microgreens are rich in antioxidants and support heart health. Perfect for salads, smoothies, and garnishing.',
    'Broccoli Microgreens': 'Mild, fresh, and highly nutritious, broccoli microgreens are packed with vitamins and detoxifying compounds. Great for daily health and immunity support.',
    'Leafypop Mix Microgreens': 'A vibrant blend of nutrient-rich microgreens packed with essential vitamins and antioxidants. Perfect for salads, sandwiches, and daily healthy meals.',
    'White Radish Microgreens': 'Crisp and slightly peppery, white radish microgreens are rich in vitamins and support digestion. Adds a fresh kick to salads and wraps.',
    'Pea Shoot Microgreens': 'Sweet, tender, and full of plant-based protein. Pea shoots are ideal for smoothies, salads, and stir-fries with a fresh green flavor.',
    'Sunflower Microgreens': 'Crunchy and nutty sunflower microgreens are loaded with nutrients and healthy fats. A perfect topping for bowls, sandwiches, and snacks.',
    # Also handle alternate names that may exist in DB
    'Radish Microgreens': 'Crisp and slightly peppery, radish microgreens are rich in vitamins and support digestion. Adds a fresh kick to salads and wraps.',
}

print("Updating product descriptions...\n")
for name, desc in descriptions.items():
    updated = Product.objects.filter(name__icontains=name.replace(' Microgreens', '').replace('Leafypop', 'Leafypop')).update(description=desc)
    if updated:
        print(f"  ✅ Updated: {name}")
    else:
        # Try a looser match
        for product in Product.objects.all():
            key = name.lower().split()[0]  # e.g. "beetroot", "broccoli"
            if key in product.name.lower():
                product.description = desc
                product.save()
                print(f"  ✅ Updated (fuzzy match): {product.name}")
                break
        else:
            print(f"  ⚠️  Not found: {name}")

print("\nAll done! Listing current products:")
for p in Product.objects.all():
    print(f"  📦 {p.name}: {p.description[:60]}...")
