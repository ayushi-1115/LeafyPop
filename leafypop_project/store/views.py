from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from .models import Product, SubscriptionPack, FAQ, UserActivity, Review
from .forms import ProductForm, FAQForm, SubscriptionPackForm, ReviewForm
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
import os

# INDEX VIEW: Fetches all data and renders the Home Page
def index(request):
    products = Product.objects.all()
    subscription_packs = SubscriptionPack.objects.all()
    faqs = FAQ.objects.all()
    reviews = Review.objects.filter(is_approved=True)[:6]  # Show only approved reviews, limit to 6
    context = {
        'products': products,
        'subscription_packs': subscription_packs,
        'faqs': faqs,
        'reviews': reviews,
    }
    return render(request, 'store/index.html', context)

# REGISTER VIEW: Handles user account creation
def register_view(request):
    if request.method == 'POST':
        # If the form is submitted (POST request)
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save() # Create the user in database
            # Log Activity
            UserActivity.objects.create(user=user, activity_type="Registration & Login")
            messages.success(request, f"Welcome to LeafyPop, {user.username}!")
            return redirect('index') # Go to home page
    else:
        # If the user is just visiting the page (GET request)
        form = UserCreationForm()
    return render(request, 'store/register.html', {'form': form})

# LOGIN VIEW: Handles user authentication
def login_view(request):
    if request.method == 'POST':
        # Get data from the submitted form
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # Check if username and password match any user in database
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user) # Start user session
                # Log Activity
                UserActivity.objects.create(user=user, activity_type="Login")
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('index')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    # Show empty login form if GET request or failed login
    form = AuthenticationForm()
    return render(request, 'store/login.html', {'form': form})

# LOGOUT VIEW: Ends user session
def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('index')

# PROFILE VIEW: Shows user information
@login_required
def profile_view(request):
    return render(request, 'store/profile.html')

# MASTER DASHBOARD: Only for SuperAdmin to see everything
@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard_view(request):
    total_users = User.objects.count()
    total_products = Product.objects.count()
    activities = UserActivity.objects.all()[:50] # Show last 50 activities
    all_users = User.objects.all().order_by('-date_joined')
    products = Product.objects.all().order_by('-created_at')
    faqs = FAQ.objects.all().order_by('order')
    subscriptions = SubscriptionPack.objects.all()
    pending_reviews = Review.objects.filter(is_approved=False).order_by('-created_at')
    approved_reviews = Review.objects.filter(is_approved=True).order_by('-created_at')
    
    context = {
        'total_users': total_users,
        'total_products': total_products,
        'activities': activities,
        'all_users': all_users,
        'products': products,
        'faqs': faqs,
        'subscriptions': subscriptions,
        'pending_reviews': pending_reviews,
        'approved_reviews': approved_reviews,
    }
    return render(request, 'store/admin_dashboard.html', context)

@user_passes_test(lambda u: u.is_superuser)
def add_product_view(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            # Log Activity
            UserActivity.objects.create(
                user=request.user, 
                activity_type="Product Created", 
                details=f"Added new product: {product.name}"
            )
            messages.success(request, "Product added successfully!")
            return redirect('master_dashboard')
    else:
        form = ProductForm()
    return render(request, 'store/product_form.html', {'form': form, 'title': 'Add New Product'})

@user_passes_test(lambda u: u.is_superuser)
def edit_product_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save()
            # Log Activity
            UserActivity.objects.create(
                user=request.user, 
                activity_type="Product Updated", 
                details=f"Updated details for: {product.name}"
            )
            messages.success(request, "Product updated successfully!")
            return redirect('master_dashboard')
    else:
        form = ProductForm(instance=product)
    return render(request, 'store/product_form.html', {'form': form, 'title': f'Edit {product.name}'})

@user_passes_test(lambda u: u.is_superuser)
def delete_product_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product_name = product.name
    if request.method == 'POST':
        product.delete()
        # Log Activity
        UserActivity.objects.create(
            user=request.user, 
            activity_type="Product Deleted", 
            details=f"Permanently deleted: {product_name}"
        )
        messages.success(request, "Product deleted successfully!")
        return redirect('master_dashboard')
    return redirect('master_dashboard')

# FAQ Views
@user_passes_test(lambda u: u.is_superuser)
def add_faq_view(request):
    if request.method == 'POST':
        form = FAQForm(request.POST)
        if form.is_valid():
            faq = form.save()
            UserActivity.objects.create(user=request.user, activity_type="FAQ Created", details=f"Added FAQ: {faq.question}")
            messages.success(request, "FAQ added successfully!")
            return redirect('master_dashboard')
    else:
        form = FAQForm()
    return render(request, 'store/faq_form.html', {'form': form, 'title': 'Add New FAQ'})

@user_passes_test(lambda u: u.is_superuser)
def edit_faq_view(request, pk):
    faq = get_object_or_404(FAQ, pk=pk)
    if request.method == 'POST':
        form = FAQForm(request.POST, instance=faq)
        if form.is_valid():
            faq = form.save()
            UserActivity.objects.create(user=request.user, activity_type="FAQ Updated", details=f"Updated FAQ: {faq.question}")
            messages.success(request, "FAQ updated successfully!")
            return redirect('master_dashboard')
    else:
        form = FAQForm(instance=faq)
    return render(request, 'store/faq_form.html', {'form': form, 'title': 'Edit FAQ'})

@user_passes_test(lambda u: u.is_superuser)
def delete_faq_view(request, pk):
    faq = get_object_or_404(FAQ, pk=pk)
    question = faq.question
    if request.method == 'POST':
        faq.delete()
        UserActivity.objects.create(user=request.user, activity_type="FAQ Deleted", details=f"Deleted FAQ: {question}")
        messages.success(request, "FAQ deleted successfully!")
    return redirect('master_dashboard')

# Subscription Views
@user_passes_test(lambda u: u.is_superuser)
def add_subscription_view(request):
    if request.method == 'POST':
        form = SubscriptionPackForm(request.POST)
        if form.is_valid():
            sub = form.save()
            UserActivity.objects.create(user=request.user, activity_type="Plan Created", details=f"Added Plan: {sub.name}")
            messages.success(request, "Subscription Plan added successfully!")
            return redirect('master_dashboard')
    else:
        form = SubscriptionPackForm()
    return render(request, 'store/subscription_form.html', {'form': form, 'title': 'Add New Subscription Plan'})

@user_passes_test(lambda u: u.is_superuser)
def edit_subscription_view(request, pk):
    sub = get_object_or_404(SubscriptionPack, pk=pk)
    if request.method == 'POST':
        form = SubscriptionPackForm(request.POST, instance=sub)
        if form.is_valid():
            sub = form.save()
            UserActivity.objects.create(user=request.user, activity_type="Plan Updated", details=f"Updated Plan: {sub.name}")
            messages.success(request, "Subscription Plan updated successfully!")
            return redirect('master_dashboard')
    else:
        form = SubscriptionPackForm(instance=sub)
    return render(request, 'store/subscription_form.html', {'form': form, 'title': f'Edit {sub.name}'})

@user_passes_test(lambda u: u.is_superuser)
def delete_subscription_view(request, pk):
    sub = get_object_or_404(SubscriptionPack, pk=pk)
    name = sub.name
    if request.method == 'POST':
        sub.delete()
        UserActivity.objects.create(user=request.user, activity_type="Plan Deleted", details=f"Deleted Plan: {name}")
        messages.success(request, "Subscription Plan deleted successfully!")
    return redirect('master_dashboard')

# REVIEW MANAGEMENT VIEWS
def submit_review_view(request):
    """Public view for customers to submit reviews"""
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.is_approved = False  # Requires admin approval
            review.save()
            messages.success(request, "Thank you! Your review has been submitted and is awaiting approval.")
            return redirect('index')
    else:
        form = ReviewForm()
    return render(request, 'store/review_form.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def approve_review_view(request, pk):
    """Admin view to approve a pending review"""
    review = get_object_or_404(Review, pk=pk)
    review.is_approved = True
    review.save()
    UserActivity.objects.create(user=request.user, activity_type="Review Approved", details=f"Approved review by {review.customer_name}")
    messages.success(request, "Review approved successfully!")
    return redirect('master_dashboard')

@user_passes_test(lambda u: u.is_superuser)
def delete_review_view(request, pk):
    """Admin view to delete a review"""
    review = get_object_or_404(Review, pk=pk)
    customer_name = review.customer_name
    if request.method == 'POST':
        review.delete()
        UserActivity.objects.create(user=request.user, activity_type="Review Deleted", details=f"Deleted review by {customer_name}")
        messages.success(request, "Review deleted successfully!")
    return redirect('master_dashboard')

from django.views.decorators.csrf import csrf_exempt

# @login_required
@csrf_exempt
def send_order_email(request):
    """
    API View to send Email notifications to admins when a user shows interest.
    """
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        order_name = data.get('name')
        order_details = data.get('details', '')
        image_url = data.get('imageUrl', '')
        custom_message = data.get('message')
        
        # Identification fields (optional)
        customer_name = data.get('customer_name', 'Anonymous')
        customer_phone = data.get('customer_phone', 'Not provided')
        
        # Build Email Content
        if custom_message:
            subject = f"💬 New Support Query from {customer_name}"
            message_body = (
                f"New Support Query:\n\n"
                f"Customer: {customer_name}\n"
                f"Phone: {customer_phone}\n"
                f"Message: {custom_message}\n"
            )
        else:
            subject = f"🚀 New Order Interest: {order_name}"
            message_body = (
                f"New Order Interest!\n\n"
                f"Product: {order_name}\n"
                f"Details: {order_details}\n"
                f"Customer: {customer_name}\n"
                f"Phone: {customer_phone}\n"
                f"Image: {image_url}\n"
            )
            
        admin_emails = ['ayushisp1115@gmail.com']

        try:
            send_mail(
                subject,
                message_body,
                settings.DEFAULT_FROM_EMAIL,
                admin_emails,
                fail_silently=False,
            )
            print(f"✅ Success! Email sent to {admin_emails}")
            return JsonResponse({
                'status': 'success', 
                'message': f'Notified admins via email successfully'
            })
        except Exception as e:
            print(f"❌ Email Error: {str(e)}")
            return JsonResponse({'status': 'error', 'message': 'Failed to send email. Check console.'}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
    