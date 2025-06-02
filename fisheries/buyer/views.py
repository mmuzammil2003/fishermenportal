from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser
from django.urls import reverse

# Create your views here.

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

@login_required
def role_redirect(request):
    if request.user.is_fisher():
        return redirect('fishportal:home')
    elif request.user.is_buyer():
        return redirect('buyer:dashboard')
    return redirect('login')

@login_required
def dashboard(request):
    if not request.user.is_buyer():
        return redirect('fishportal:home')
    return render(request, 'buyer/dashboard.html')
