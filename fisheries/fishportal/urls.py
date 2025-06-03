from django.urls import path
from . import views

app_name = 'fishportal'

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.home, name='dashboard'),
    path('my-catches/', views.my_catches, name='my_catches'),
    path('upload-catch/', views.upload_catch, name='upload_catch'),
    path('edit-catch/<int:catch_id>/', views.edit_catch, name='edit_catch'),
    path('delete-catch/<int:catch_id>/', views.delete_catch, name='delete_catch'),
    path('inventory/', views.inventory, name='inventory'),
    path('pricing-trends/', views.pricing_trends, name='pricing_trends'),
]
