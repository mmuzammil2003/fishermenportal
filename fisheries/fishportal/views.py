from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView

class DashboardView(TemplateView):
    template_name = "fishportal/home.html"

class UploadCatchView(TemplateView):
    def get(self, request):
        return render(request, 'fishportal/upload.html')

class InventoryView(TemplateView):
    template_name = "fishportal/inventory.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Sample stats data
        context['stats'] = [
            {
                'title': 'Total Inventory',
                'value': '2,534 kg',
                'change': '+12.5%',
                'color': 'blue',
                'icon': '<svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"></path></svg>'
            },
            {
                'title': 'Active Listings',
                'value': '186',
                'change': '+8.2%',
                'color': 'emerald',
                'icon': '<svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path></svg>'
            },
            {
                'title': 'Average Price',
                'value': '$24.50/kg',
                'change': '+2.3%',
                'color': 'purple',
                'icon': '<svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>'
            },
            {
                'title': 'Total Revenue',
                'value': '$62,084',
                'change': '+15.3%',
                'color': 'amber',
                'icon': '<svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path></svg>'
            }
        ]
        
        # Sample inventory data
        context['inventory'] = [
            {
                'fishType': 'Atlantic Salmon',
                'status': 'Available',
                'location': 'North Atlantic',
                'weight': '125 kg',
                'quality': 'Premium',
                'price': '32.50',
                'freshness': 95,
                'views': 234,
                'likes': 45,
                'image': 'https://source.unsplash.com/800x600/?salmon'
            },
            {
                'fishType': 'Bluefin Tuna',
                'status': 'Available',
                'location': 'Pacific Ocean',
                'weight': '180 kg',
                'quality': 'Grade A',
                'price': '45.75',
                'freshness': 88,
                'views': 312,
                'likes': 67,
                'image': 'https://source.unsplash.com/800x600/?tuna'
            },
            {
                'fishType': 'Red Snapper',
                'status': 'Sold',
                'location': 'Caribbean Sea',
                'weight': '75 kg',
                'quality': 'Premium',
                'price': '28.90',
                'freshness': 92,
                'views': 178,
                'likes': 34,
                'image': 'https://source.unsplash.com/800x600/?snapper'
            }
        ]
        
        return context
