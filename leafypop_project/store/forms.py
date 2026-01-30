from django import forms
from .models import Product, FAQ, SubscriptionPack, Review

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price_50g', 'price_100g', 'is_in_stock', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-green-500 focus:bg-white transition-all font-bold text-sm', 'placeholder': 'e.g. Broccoli Microgreens'}),
            'description': forms.Textarea(attrs={'class': 'w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-green-500 focus:bg-white transition-all text-sm', 'rows': 4, 'placeholder': 'Briefly describe your product details...'}),
            'price_50g': forms.NumberInput(attrs={'class': 'w-full pl-8 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-green-500 focus:bg-white transition-all font-bold text-sm', 'placeholder': '0.00'}),
            'price_100g': forms.NumberInput(attrs={'class': 'w-full pl-8 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-green-500 focus:bg-white transition-all font-bold text-sm', 'placeholder': '0.00'}),
            'is_in_stock': forms.CheckboxInput(attrs={'class': 'w-6 h-6 text-green-600 rounded-lg focus:ring-green-500 border-gray-300 transition-all cursor-pointer accent-green-600'}),
            'image': forms.FileInput(attrs={'class': 'w-full text-sm text-gray-400 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-xs file:font-black file:uppercase file:bg-green-50 file:text-green-700 hover:file:bg-green-100 transition-all'}),
        }

class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ['question', 'answer', 'order']
        widgets = {
            'question': forms.TextInput(attrs={'class': 'w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-green-500 focus:bg-white transition-all font-bold text-sm', 'placeholder': 'e.g. How do I store microgreens?'}),
            'answer': forms.Textarea(attrs={'class': 'w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-green-500 focus:bg-white transition-all text-sm', 'rows': 4, 'placeholder': 'Provide a helpful answer...'}),
            'order': forms.NumberInput(attrs={'class': 'w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-green-500 focus:bg-white transition-all font-bold text-sm', 'placeholder': '0'}),
        }

class SubscriptionPackForm(forms.ModelForm):
    class Meta:
        model = SubscriptionPack
        fields = ['name', 'description', 'one_time_price', 'monthly_plan_price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-green-500 focus:bg-white transition-all font-bold text-sm', 'placeholder': 'e.g. Family Pack'}),
            'description': forms.Textarea(attrs={'class': 'w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-green-500 focus:bg-white transition-all text-sm', 'rows': 4, 'placeholder': 'Describe what is included...'}),
            'one_time_price': forms.NumberInput(attrs={'class': 'w-full pl-8 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-green-500 focus:bg-white transition-all font-bold text-sm', 'placeholder': '0.00'}),
            'monthly_plan_price': forms.NumberInput(attrs={'class': 'w-full pl-8 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-green-500 focus:bg-white transition-all font-bold text-sm', 'placeholder': '0.00'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['customer_name', 'rating', 'review_text']
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-green-500 focus:bg-white transition-all font-bold text-sm', 'placeholder': 'Your name'}),
            'rating': forms.RadioSelect(attrs={'class': 'rating-radio'}),
            'review_text': forms.Textarea(attrs={'class': 'w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-green-500 focus:bg-white transition-all text-sm', 'rows': 4, 'placeholder': 'Share your experience with LeafyPop products...'}),
        }

