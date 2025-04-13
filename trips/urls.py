from django.urls import path
from . import views

urlpatterns = [
    path('new/', views.create_trip, name='create_trip'),
    path('list/', views.trip_list, name='trip_list'),
    path('<int:trip_id>/', views.trip_detail, name='trip_detail'),
    path('<int:trip_id>/delete/', views.delete_trip, name='delete_trip'),
    path('<int:trip_id>/packing/', views.packing_list, name='packing_list'),
    path('<int:trip_id>/update/', views.update_packing_list, name='update_packing_list'),
    path('feedback/', views.leave_feedback, name='leave_feedback'),
]