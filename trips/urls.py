from django.urls import path
from . import views

urlpatterns = [
    path('new/', views.create_trip, name='create_trip'),
    path('list/', views.trip_list, name='trip_list'),
]