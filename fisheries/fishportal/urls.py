# fishportal/urls.py

from django.urls import path
from .views import DashboardView, UploadCatchView, InventoryView

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('upload/', UploadCatchView.as_view(), name='upload_catch'),
    path('inventory/', InventoryView.as_view(), name='inventory'),
]
