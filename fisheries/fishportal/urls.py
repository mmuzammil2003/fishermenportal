# fishportal/urls.py

from django.urls import path
from .views import DashboardView
from .views import UploadCatchView

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('upload/', UploadCatchView.as_view(), name='upload_catch'),
]
