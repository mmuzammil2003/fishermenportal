from django.urls import path
from . import views

app_name = 'buyer'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
] 