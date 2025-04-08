from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Trip
from .forms import TripForm
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

@login_required
def delete_trip(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id, user=request.user)
    
    if request.method == 'POST':
        trip.delete()
        messages.success(request, 'Trip deleted successfully.')
        return redirect('trip_list')
    
    return render(request, 'trips/confirm_delete.html', {'trip': trip})

@login_required
def create_trip(request):
    if request.method == 'POST':
        form = TripForm(request.POST)
        if form.is_valid():
            trip = form.save(commit=False)
            trip.user = request.user
            trip.save()
            return redirect('trip_list')
    else:
        form = TripForm()
    return render(request, 'trips/create_trip.html', {'form': form})

@login_required
def trip_list(request):
    trips = Trip.objects.filter(user=request.user).order_by('-start_date')
    return render(request, 'trips/trip_list.html', {'trips': trips})

@login_required
def trip_detail(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id, user=request.user)
    return render(request, 'trips/trip_detail.html', {'trip': trip})