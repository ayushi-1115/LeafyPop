from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), # Home Page
    path('register/', views.register_view, name='register'), # Sign Up Page
    path('login/', views.login_view, name='login'), # Login Page
    path('logout/', views.logout_view, name='logout'), # Logout Action
]
