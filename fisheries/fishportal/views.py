# fishportal/views.py

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import TemplateView

class DashboardView(TemplateView):
    template_name = "fishportal/home.html"

