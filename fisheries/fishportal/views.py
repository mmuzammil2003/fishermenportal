from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

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
class UploadCatchView(TemplateView):
    template_name = 'fishportal/upload_catch.html'

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

# Function-based views for URL patterns
home = HomeView.as_view()
upload_catch = UploadCatchView.as_view()
inventory = InventoryView.as_view()
pricing_trends = PricingTrendsView.as_view()
