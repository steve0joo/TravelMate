from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

class Trip(models.Model):
    TRIP_TYPE_CHOICES = [
        ('beach', 'Beach'),
        ('city', 'City'),
        ('hiking', 'Hiking'),
        ('business', 'Business'),
        ('snow', 'Snow / Ski'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    trip_type = models.CharField(max_length=50, choices=TRIP_TYPE_CHOICES, default='other')
    manually_cleared = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class PackingItem(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='packing_items')
    name = models.CharField(max_length=100)
    is_packed = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class Feedback(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.user.username} at {self.created_at}"