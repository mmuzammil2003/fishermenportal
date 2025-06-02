from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser

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
        return redirect('market')  # Fisher redirected to market view
    elif request.user.is_buyer():
        return redirect('buyers')  # Buyer redirected to buyers view
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
