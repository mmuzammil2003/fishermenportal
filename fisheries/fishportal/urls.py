from django.urls import path
from . import views

app_name = 'fishportal'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('upload-catch/', views.upload_catch, name='upload_catch'),
    path('my-catches/', views.my_catches, name='my_catches'),
    path('edit-catch/<int:catch_id>/', views.edit_catch, name='edit_catch'),
    path('delete-catch/<int:catch_id>/', views.delete_catch, name='delete_catch'),
    path('inventory/', views.inventory, name='inventory'),
    path('pricing-trends/', views.pricing_trends, name='pricing_trends'),
]
