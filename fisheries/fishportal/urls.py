from django.urls import path
from . import views

app_name = 'fishportal'

urlpatterns = [
    path('', views.home, name='home'),
    path('upload-catch/', views.upload_catch, name='upload_catch'),
    path('inventory/', views.inventory, name='inventory'),
    path('pricing-trends/', views.pricing_trends, name='pricing_trends'),
]
