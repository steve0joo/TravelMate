from django.urls import path
from . import views
from trips.views import shared_trip_view

urlpatterns = [
    path('new/', views.create_trip, name='create_trip'),
    path('list/', views.trip_list, name='trip_list'),
    path('<int:trip_id>/', views.trip_detail, name='trip_detail'),
    path('<int:trip_id>/delete/', views.delete_trip, name='delete_trip'),
    path('<int:trip_id>/packing/', views.packing_list, name='packing_list'),
    path('<int:trip_id>/update/', views.update_packing_list, name='update_packing_list'),
    path('feedback/', views.leave_feedback, name='leave_feedback'),
    path('<int:trip_id>/toggle_public/', views.toggle_public_trip, name='toggle_public'),
    path('shared/<str:share_token>/', shared_trip_view, name='shared_trip'),
    path('download/<int:trip_id>/', views.download_trip_txt, name='download_trip'),
    path('share/<int:trip_id>/', views.share_trip, name='share_trip'),
]