from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, SubscriptionPack, FAQ

# INDEX VIEW: Fetches all data and renders the Home Page
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

# REGISTER VIEW: Handles user account creation
def register_view(request):
    if request.method == 'POST':
        # If the form is submitted (POST request)
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save() # Create the user in database
            login(request, user) # Automatically log the user in after signup
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
    