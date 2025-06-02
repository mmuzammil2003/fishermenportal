from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count, Sum
from django.utils import timezone
from datetime import timedelta
from django.db import transaction
from decimal import Decimal, InvalidOperation
from .models import CustomUser, Order, Transaction
from fishportal.models import FishCatch
from django.contrib.auth.views import LoginView

# Registration view
def register_view(request):
    user_type = request.GET.get('type', '').upper()
    if user_type not in ['FISHER', 'BUYER']:
        return redirect('login')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        user_type = request.POST.get('user_type')

        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'registration/register.html', {'user_type': user_type})

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'registration/register.html', {'user_type': user_type})

        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password1,
            user_type=user_type,
            phone=phone,
            address=address
        )
        login(request, user)
        return redirect('role_redirect')

    return render(request, 'registration/register.html', {'user_type': user_type})

# Role redirect view
@login_required
def role_redirect(request):
    if request.user.is_fisher():
        return redirect('fishportal:dashboard')  # Redirect fisher to fishportal dashboard
    elif request.user.is_buyer():
        return redirect('buyer:dashboard')  # Redirect buyer to buyer dashboard
    return redirect('login')

# Buyer dashboard view (if needed)
@login_required
def dashboard_view(request):
    if not request.user.is_buyer():
        return redirect('login')  # Prevent unauthorized access
    return render(request, 'dashboard.html')

# Buyers.html view
@login_required
def buyers_view(request):
    if not request.user.is_buyer():
        return redirect('login')
    return render(request, 'buyers.html')

# Market.html view
@login_required
def market_view(request):
    if not request.user.is_fisher():
        return redirect('login')
    return render(request, 'market.html')

@login_required
def dashboard(request):
    # Get order statistics
    total_orders = Order.objects.filter(buyer=request.user).count()
    pending_orders = Order.objects.filter(buyer=request.user, status='PENDING').count()
    completed_orders = Order.objects.filter(buyer=request.user, status='COMPLETED').count()
    
    # Get total spent amount
    total_spent = Order.objects.filter(
        buyer=request.user, 
        status='COMPLETED'
    ).aggregate(total=Sum('total_price'))['total'] or 0
    
    # Get recent orders with more details
    recent_orders = Order.objects.filter(buyer=request.user).select_related('fish_catch').order_by('-created_at')[:5]
    
    context = {
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'completed_orders': completed_orders,
        'total_spent': total_spent,
        'recent_orders': recent_orders,
    }
    return render(request, 'buyer/dashboard.html', context)

@login_required
def available_catches(request):
    if not request.user.is_buyer():
        return redirect('login')
    
    # Get filter parameters
    fish_type = request.GET.get('fish_type')
    quality_grade = request.GET.get('quality_grade')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    sort_by = request.GET.get('sort_by', '-timestamp')  # Default sort by newest
    
    # Base queryset of unsold catches
    catches = FishCatch.objects.filter(is_sold=False)
    
    # Apply filters
    if fish_type:
        catches = catches.filter(fish_type=fish_type)
    if quality_grade:
        catches = catches.filter(quality_grade=quality_grade)
    if min_price:
        catches = catches.filter(price_per_kg__gte=float(min_price))
    if max_price:
        catches = catches.filter(price_per_kg__lte=float(max_price))
    
    # Apply sorting
    valid_sort_fields = ['price_per_kg', '-price_per_kg', 'timestamp', '-timestamp', 'weight', '-weight']
    if sort_by in valid_sort_fields:
        catches = catches.order_by(sort_by)
    
    # Get unique values for filters
    fish_types = FishCatch.objects.values_list('fish_type', flat=True).distinct()
    quality_grades = FishCatch.objects.values_list('quality_grade', flat=True).distinct()
    
    # Pagination
    paginator = Paginator(catches, 9)  # Show 9 catches per page
    page = request.GET.get('page')
    catches = paginator.get_page(page)
    
    context = {
        'catches': catches,
        'fish_types': fish_types,
        'quality_grades': quality_grades,
        'current_filters': {
            'fish_type': fish_type,
            'quality_grade': quality_grade,
            'min_price': min_price,
            'max_price': max_price,
            'sort_by': sort_by,
        }
    }
    return render(request, 'buyer/available_catches.html', context)

@login_required
def my_orders(request):
    # Get filter parameters
    status = request.GET.get('status')
    time_period = request.GET.get('time_period')
    sort_by = request.GET.get('sort', '-created_at')  # Default to newest first
    
    # Base queryset with related fish_catch
    orders = Order.objects.filter(buyer=request.user).select_related('fish_catch')
    
    # Apply filters
    if status:
        orders = orders.filter(status=status)
    
    if time_period:
        now = timezone.now()
        if time_period == 'today':
            orders = orders.filter(created_at__date=now.date())
        elif time_period == 'week':
            orders = orders.filter(created_at__gte=now - timedelta(days=7))
        elif time_period == 'month':
            orders = orders.filter(created_at__gte=now - timedelta(days=30))
        elif time_period == 'year':
            orders = orders.filter(created_at__gte=now - timedelta(days=365))
    
    # Apply sorting
    valid_sort_fields = ['created_at', '-created_at', 'total_price', '-total_price']
    if sort_by in valid_sort_fields:
        orders = orders.order_by(sort_by)
    else:
        orders = orders.order_by('-created_at')  # Default sort
    
    # Pagination
    paginator = Paginator(orders, 10)  # Show 10 orders per page
    page = request.GET.get('page')
    orders = paginator.get_page(page)
    
    context = {
        'orders': orders,
    }
    return render(request, 'buyer/my_orders.html', context)

@login_required
def create_order(request, catch_id):
    if not request.user.is_buyer():
        messages.error(request, 'Only buyers can place orders.')
        return redirect('login')

    if request.method == 'POST':
        catch = get_object_or_404(FishCatch, id=catch_id)
        
        try:
            quantity = Decimal(request.POST.get('quantity', '0'))
        except InvalidOperation:
            messages.error(request, 'Please enter a valid quantity.')
            return redirect('buyer:available_catches')
        
        # Validate quantity
        if quantity <= 0:
            messages.error(request, 'Please specify a valid quantity greater than 0.')
            return redirect('buyer:available_catches')
        
        if quantity > catch.weight:
            messages.error(request, f'Only {catch.weight}kg available.')
            return redirect('buyer:available_catches')
        
        # Check if catch is still available
        if catch.is_sold:
            messages.error(request, 'This catch is no longer available.')
            return redirect('buyer:available_catches')
        
        try:
            with transaction.atomic():
                # Calculate total price
                total_price = quantity * Decimal(str(catch.price_per_kg))
                
                # Create order
                order = Order.objects.create(
                    buyer=request.user,
                    fish_catch=catch,
                    quantity=quantity,
                    total_price=total_price,
                    status='PENDING'
                )
                
                # Update catch quantity
                catch.weight = catch.weight - quantity
                if catch.weight == 0:
                    catch.is_sold = True
                catch.save()
                
                # Create transaction record
                Transaction.objects.create(
                    order=order,
                    amount=total_price,
                    transaction_type='ORDER_PLACED'
                )
                
                messages.success(request, 'Order placed successfully! You can track its status in My Orders.')
                return redirect('buyer:my_orders')
                
        except Exception as e:
            messages.error(request, 'An error occurred while placing your order. Please try again.')
            return redirect('buyer:available_catches')
    
    return redirect('buyer:available_catches')

@login_required
def cancel_order(request, order_id):
    if not request.user.is_buyer():
        messages.error(request, 'Only buyers can cancel orders.')
        return redirect('login')

    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id, buyer=request.user, status='PENDING')
        
        try:
            with transaction.atomic():
                # Return the quantity to the catch
                catch = order.fish_catch
                catch.weight += order.quantity
                catch.is_sold = False
                catch.save()
                
                # Update order status
                order.status = 'CANCELLED'
                order.save()
                
                # Create transaction record
                Transaction.objects.create(
                    order=order,
                    amount=order.total_price,
                    transaction_type='ORDER_CANCELLED'
                )
                
                messages.success(request, 'Order cancelled successfully!')
        except Exception as e:
            messages.error(request, 'An error occurred while cancelling your order. Please try again.')
    
    return redirect('buyer:my_orders')

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    
    def form_valid(self, form):
        user_type = self.request.POST.get('user_type')
        user = form.get_user()
        
        if not user_type:
            form.add_error(None, 'Please select your role')
            return self.form_invalid(form)
        
        if user_type == 'FISHER' and not user.is_fisher():
            form.add_error(None, 'This account is not registered as a fisher')
            return self.form_invalid(form)
        elif user_type == 'BUYER' and not user.is_buyer():
            form.add_error(None, 'This account is not registered as a buyer')
            return self.form_invalid(form)
        
        login(self.request, user)
        return redirect('role_redirect')
