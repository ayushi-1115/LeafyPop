from django.shortcuts import render
from .models import Product, SubscriptionPack, FAQ

def index(request):
    products = Product.objects.all()
    subscription_packs = SubscriptionPack.objects.all()
    faqs = FAQ.objects.all()
    context = {
        'products': products,
        'subscription_packs': subscription_packs,
        'faqs': faqs,
    }
    return render(request, 'store/index.html', context)
    