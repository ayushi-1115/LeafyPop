from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), # Home Page
    path('register/', views.register_view, name='register'), # Sign Up Page
    path('login/', views.login_view, name='login'), # Login Page
    path('logout/', views.logout_view, name='logout'), # Logout Action
    path('profile/', views.profile_view, name='profile'), # User Dashboard
    path('master-dashboard/', views.admin_dashboard_view, name='master_dashboard'), # Superuser Dashboard
    path('master-dashboard/add-product/', views.add_product_view, name='add_product'),
    path('master-dashboard/edit-product/<int:pk>/', views.edit_product_view, name='edit_product'),
    path('master-dashboard/delete-product/<int:pk>/', views.delete_product_view, name='delete_product'),
    
    path('master-dashboard/add-faq/', views.add_faq_view, name='add_faq'),
    path('master-dashboard/edit-faq/<int:pk>/', views.edit_faq_view, name='edit_faq'),
    path('master-dashboard/delete-faq/<int:pk>/', views.delete_faq_view, name='delete_faq'),

    path('master-dashboard/add-plan/', views.add_subscription_view, name='add_subscription'),
    path('master-dashboard/edit-plan/<int:pk>/', views.edit_subscription_view, name='edit_subscription'),
    path('master-dashboard/delete-plan/<int:pk>/', views.delete_subscription_view, name='delete_subscription'),
    
    # Review URLs
    path('submit-review/', views.submit_review_view, name='submit_review'),
    path('master-dashboard/approve-review/<int:pk>/', views.approve_review_view, name='approve_review'),
    path('master-dashboard/delete-review/<int:pk>/', views.delete_review_view, name='delete_review'),
]
