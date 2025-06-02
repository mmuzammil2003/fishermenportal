from django.contrib import admin
from .models import CustomUser, Order, Transaction

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type', 'phone')
    list_filter = ('user_type',)
    search_fields = ('username', 'email', 'phone')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyer', 'fish_catch', 'quantity', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('buyer__username', 'fish_catch__fish_type')
    date_hierarchy = 'created_at'

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'order', 'amount', 'payment_method', 'payment_status', 'timestamp')
    list_filter = ('payment_status', 'payment_method', 'timestamp')
    search_fields = ('transaction_id', 'order__buyer__username')
