from django.shortcuts import render
from .models import Product, SubscriptionPack

def index(request):
    products = Product.objects.all()
    subscription_packs = SubscriptionPack.objects.all()
    context = {
        'products': products,
        'subscription_packs': subscription_packs,
    }
    return render(request, 'store/index.html', context)
    