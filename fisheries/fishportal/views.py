from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from .models import FishCatch
from django.db.models import Sum, Avg, Min, Max

@method_decorator(login_required, name='dispatch')
class HomeView(TemplateView):
    template_name = 'fishportal/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'total_catch': 156,
            'revenue': 2340,
            'active_listings': 12,
            'rating': 4.8,
        })
        return context

@method_decorator(login_required, name='dispatch')
class InventoryView(TemplateView):
    template_name = 'fishportal/inventory.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Stats data
        context['stats'] = [
            {
                'title': 'Total Catch',
                'value': '2,450 kg',
                'change': '+12%',
                'color': 'blue',
                'icon': '🐟'
            },
            {
                'title': 'Active Listings',
                'value': '24',
                'change': '+3',
                'color': 'emerald',
                'icon': '📦'
            },
            {
                'title': 'Revenue',
                'value': '$12,450',
                'change': '+18%',
                'color': 'purple',
                'icon': '💰'
            },
            {
                'title': 'Average Rating',
                'value': '4.8',
                'change': '+0.2',
                'color': 'yellow',
                'icon': '⭐'
            }
        ]

        # Sample inventory data
        context['inventory'] = [
            {
                'fishType': 'Salmon',
                'weight': '25 kg',
                'quality': 'Premium',
                'price': 45,
                'status': 'Available',
                'location': 'North Pacific',
                'freshness': 95,
                'views': 124,
                'likes': 45,
                'image': 'https://placehold.co/600x400/png?text=Salmon'
            },
            {
                'fishType': 'Tuna',
                'weight': '40 kg',
                'quality': 'Grade A',
                'price': 35,
                'status': 'Reserved',
                'location': 'South Pacific',
                'freshness': 88,
                'views': 98,
                'likes': 32,
                'image': 'https://placehold.co/600x400/png?text=Tuna'
            },
            {
                'fishType': 'Cod',
                'weight': '30 kg',
                'quality': 'Grade A',
                'price': 28,
                'status': 'Available',
                'location': 'North Atlantic',
                'freshness': 92,
                'views': 76,
                'likes': 28,
                'image': 'https://placehold.co/600x400/png?text=Cod'
            }
        ]
        return context

@method_decorator(login_required, name='dispatch')
class PricingTrendsView(TemplateView):
    template_name = 'fishportal/pricing_trends.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['market_prices'] = [
            {'fish': 'Salmon', 'price': 45},
            {'fish': 'Tuna', 'price': 35},
            {'fish': 'Cod', 'price': 28},
            {'fish': 'Halibut', 'price': 52}
        ]
        return context

@login_required
def dashboard(request):
    if not request.user.is_fisher():
        return redirect('login')
    
    # Get fisher's statistics
    total_catches = FishCatch.objects.filter(fisher=request.user).count()
    active_catches = FishCatch.objects.filter(fisher=request.user, is_sold=False).count()
    sold_catches = FishCatch.objects.filter(fisher=request.user, is_sold=True).count()
    
    # Get recent catches
    recent_catches = FishCatch.objects.filter(fisher=request.user).order_by('-timestamp')[:5]
    
    context = {
        'total_catches': total_catches,
        'active_catches': active_catches,
        'sold_catches': sold_catches,
        'recent_catches': recent_catches,
    }
    return render(request, 'fishportal/dashboard.html', context)

@login_required
def upload_catch(request):
    if not request.user.is_fisher():
        return redirect('login')
    
    if request.method == 'POST':
        try:
            # Get form data
            fish_type = request.POST.get('fish_type')
            weight = request.POST.get('weight')
            quality_grade = request.POST.get('quality_grade')
            location = request.POST.get('location')
            price_per_kg = request.POST.get('price_per_kg')
            photo = request.FILES.get('photo')
            
            # Validate required fields
            if not all([fish_type, weight, quality_grade, location, price_per_kg, photo]):
                messages.error(request, 'All fields are required')
                return render(request, 'fishportal/upload_catch.html')
            
            # Create new catch
            catch = FishCatch.objects.create(
                fisher=request.user,
                fish_type=fish_type,
                weight=float(weight),
                quality_grade=quality_grade,
                location=location,
                price_per_kg=float(price_per_kg),
                photo=photo
            )
            
            messages.success(request, 'Catch uploaded successfully!')
            return redirect('fishportal:my_catches')
            
        except Exception as e:
            messages.error(request, f'Error uploading catch: {str(e)}')
            return render(request, 'fishportal/upload_catch.html')
    
    return render(request, 'fishportal/upload_catch.html')

@login_required
def my_catches(request):
    if not request.user.is_fisher():
        return redirect('login')
    
    # Get filter parameters
    status = request.GET.get('status')
    
    # Base queryset
    catches = FishCatch.objects.filter(fisher=request.user)
    
    # Apply filters
    if status == 'active':
        catches = catches.filter(is_sold=False)
    elif status == 'sold':
        catches = catches.filter(is_sold=True)
    
    # Order by most recent
    catches = catches.order_by('-timestamp')
    
    # Pagination
    paginator = Paginator(catches, 10)  # Show 10 catches per page
    page = request.GET.get('page')
    catches = paginator.get_page(page)
    
    context = {
        'catches': catches,
    }
    return render(request, 'fishportal/my_catches.html', context)

@login_required
def inventory(request):
    if not request.user.is_fisher():
        return redirect('login')
    
    # Get inventory statistics
    inventory_stats = FishCatch.objects.filter(fisher=request.user, is_sold=False).values('fish_type').annotate(
        total_weight=Sum('weight'),
        avg_price=Avg('price_per_kg')
    )
    
    context = {
        'inventory_stats': inventory_stats,
    }
    return render(request, 'fishportal/inventory.html', context)

@login_required
def pricing_trends(request):
    if not request.user.is_fisher():
        return redirect('login')
    
    # Get pricing trends data
    # This is a placeholder - you might want to implement more sophisticated trend analysis
    trends = FishCatch.objects.filter(is_sold=True).values('fish_type').annotate(
        avg_price=Avg('price_per_kg'),
        min_price=Min('price_per_kg'),
        max_price=Max('price_per_kg')
    )
    
    context = {
        'trends': trends,
    }
    return render(request, 'fishportal/pricing_trends.html', context)

@login_required
def edit_catch(request, catch_id):
    if not request.user.is_fisher():
        return redirect('login')
    
    # Get the catch or return 404
    catch = get_object_or_404(FishCatch, id=catch_id, fisher=request.user)
    
    if request.method == 'POST':
        try:
            # Get form data
            fish_type = request.POST.get('fish_type')
            weight = request.POST.get('weight')
            quality_grade = request.POST.get('quality_grade')
            location = request.POST.get('location')
            price_per_kg = request.POST.get('price_per_kg')
            photo = request.FILES.get('photo')
            
            # Validate required fields
            if not all([fish_type, weight, quality_grade, location, price_per_kg]):
                messages.error(request, 'All fields except photo are required')
                return render(request, 'fishportal/edit_catch.html', {'catch': catch})
            
            # Update catch
            catch.fish_type = fish_type
            catch.weight = float(weight)
            catch.quality_grade = quality_grade
            catch.location = location
            catch.price_per_kg = float(price_per_kg)
            if photo:
                catch.photo = photo
            catch.save()
            
            messages.success(request, 'Catch updated successfully!')
            return redirect('fishportal:my_catches')
            
        except Exception as e:
            messages.error(request, f'Error updating catch: {str(e)}')
            return render(request, 'fishportal/edit_catch.html', {'catch': catch})
    
    return render(request, 'fishportal/edit_catch.html', {'catch': catch})

@login_required
def delete_catch(request, catch_id):
    if not request.user.is_fisher():
        return redirect('login')
    
    # Get the catch or return 404
    catch = get_object_or_404(FishCatch, id=catch_id, fisher=request.user)
    
    if request.method == 'POST':
        try:
            # Only allow deletion if the catch hasn't been sold
            if catch.is_sold:
                messages.error(request, 'Cannot delete a sold catch')
            else:
                catch.delete()
                messages.success(request, 'Catch deleted successfully!')
        except Exception as e:
            messages.error(request, f'Error deleting catch: {str(e)}')
    
    return redirect('fishportal:my_catches')

# Function-based views for URL patterns
home = HomeView.as_view()
inventory = InventoryView.as_view()
pricing_trends = PricingTrendsView.as_view()
