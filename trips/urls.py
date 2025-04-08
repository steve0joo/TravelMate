from django.urls import path
from . import views

urlpatterns = [
    path('new/', views.create_trip, name='create_trip'),
    path('list/', views.trip_list, name='trip_list'),
    path('<int:trip_id>/', views.trip_detail, name='trip_detail'),
    path('<int:trip_id>/delete/', views.delete_trip, name='delete_trip'),
]