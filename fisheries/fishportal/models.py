from django.db import models
from django.conf import settings

# Create your models here.

class FishCatch(models.Model):
    QUALITY_CHOICES = [
        ('A', 'Premium'),
        ('B', 'Standard'),
        ('C', 'Economy'),
    ]
    
    fisher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fish_type = models.CharField(max_length=100)
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    quality_grade = models.CharField(max_length=1, choices=QUALITY_CHOICES)
    location = models.CharField(max_length=200)
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.ImageField(upload_to='catch_photos/')
    timestamp = models.DateTimeField(auto_now_add=True)
    is_sold = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.fish_type} - {self.weight}kg by {self.fisher.username}"
    
    class Meta:
        ordering = ['-timestamp']
