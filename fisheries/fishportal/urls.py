from django.urls import path
from . import views

app_name = 'fishportal'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('inventory/', views.InventoryView.as_view(), name='inventory'),
    path('upload-catch/', views.UploadCatchView.as_view(), name='upload_catch'),
    path('pricing-trends/', views.PricingTrendsView.as_view(), name='pricing_trends'),
]
