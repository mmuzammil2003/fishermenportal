from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView

class DashboardView(TemplateView):
    template_name = "fishportal/home.html"

class UploadCatchView(TemplateView):
    def get(self, request):
        return render(request, 'fishportal/upload.html')
