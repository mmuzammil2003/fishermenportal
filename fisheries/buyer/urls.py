from django.urls import path
from . import views

app_name = 'buyer'  # use this if you're namespacing

urlpatterns = [
    path('', views.dashboard, name='dashboard'),  # Make dashboard the default view
    path('available-catches/', views.available_catches, name='available_catches'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('create-order/<int:catch_id>/', views.create_order, name='create_order'),
    path('cancel-order/<int:order_id>/', views.cancel_order, name='cancel_order'),
]
