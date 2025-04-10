from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from trips.utils import generate_packing_list
from .models import PackingItem, Trip
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

@login_required
def packing_list(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id, user=request.user)
    generate_packing_list(trip)

    if request.method == 'POST':
        new_item = request.POST.get('new_item')
        if new_item:
            PackingItem.objects.create(trip=trip, name=new_item)

    items = trip.packing_items.all().order_by('is_packed', 'name')
    return render(request, 'trips/packing_list.html', {'trip': trip, 'items': items})

@login_required
def update_packing_list(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id, user=request.user)

    if request.method == 'POST':
        packed_items = request.POST.getlist('packed_items')
        delete_item = request.POST.get('delete_item')
        new_item = request.POST.get('new_item')

        # Delete item if requested
        if delete_item:
            trip.packing_items.filter(name=delete_item).delete()

        # Add a new custom item
        elif new_item:
            if not trip.packing_items.filter(name=new_item).exists():
                PackingItem.objects.create(trip=trip, name=new_item)

        else:
            # Update packed state for all items
            for item in trip.packing_items.all():
                item.is_packed = item.name in packed_items
                item.save()

    return redirect('packing_list', trip_id=trip.id)