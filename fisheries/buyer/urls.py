from django.urls import path
from . import views

app_name = 'buyer'  # use this if you're namespacing

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('role-redirect/', views.role_redirect, name='role_redirect'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('market/', views.market_view, name='market'),
    
]
