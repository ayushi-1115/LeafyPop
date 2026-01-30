import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'leafypop_project.settings')
django.setup()

from store.models import FAQ

faqs = [
    {
        "question": "What is LeafyPop?",
        "answer": "LeafyPop is an eco-friendly platform offering fresh, natural, and sustainably grown plant-based products and microgreens for a healthier lifestyle."
    },
    {
        "question": "What are microgreens?",
        "answer": "Microgreens are young vegetable greens harvested just after sprouting. They are rich in nutrients, vitamins, and antioxidants."
    },
    {
        "question": "Are your products organically grown?",
        "answer": "Yes! All LeafyPop products are grown using natural and sustainable methods without harmful chemicals."
    },
    {
        "question": "How fresh are the products?",
        "answer": "Our microgreens are harvested only after you place an order to ensure maximum freshness and nutrition."
    },
    {
        "question": "How do I place an order?",
        "answer": "Simply browse our products, add items to your cart, and proceed to checkout to place your order."
    },
    {
        "question": "Do you deliver to my location?",
        "answer": "Currently, we deliver within selected cities. Delivery areas will expand soon."
    },
    {
        "question": "How should I store microgreens?",
        "answer": "Store them in an airtight container in the refrigerator. Consume within 3–5 days for best taste and nutrition."
    },
    {
        "question": "Are your packaging materials eco-friendly?",
        "answer": "Yes! We use biodegradable and recyclable packaging materials to reduce environmental impact."
    },

]

for i, faq_data in enumerate(faqs):
    faq, created = FAQ.objects.get_or_create(
        question=faq_data['question'],
        defaults={'answer': faq_data['answer'], 'order': i}
    )
    if not created:
        faq.answer = faq_data['answer']
        faq.order = i
        faq.save()
    print(f"{'Created' if created else 'Updated'} FAQ: {faq.question}")

print("FAQ population complete!")
