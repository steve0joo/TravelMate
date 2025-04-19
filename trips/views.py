from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from trips.utils import generate_packing_list
from .models import PackingItem, Trip
from .forms import TripForm
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

from .forms import FeedbackForm
from .models import Feedback
from django.shortcuts import render, get_object_or_404
from .models import Trip

from django.http import HttpResponse
from .models import Trip, PackingItem

import requests
from .utils import get_place_recommendations

def share_trip(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)

    packing_items = PackingItem.objects.filter(trip=trip)
    packing_list_text = "\n".join(f"- {item.name}" for item in packing_items)

    content = (
        f"Trip Name: {trip.name}\n"
        f"Destination: {trip.destination}\n"
        f"Start Date: {trip.start_date}\n"
        f"End Date: {trip.end_date}\n\n"
        f"Packing List:\n{packing_list_text}"
    )

    return render(request, 'trips/share_trip.html', {
        'trip': trip,
        'trip_text': content,
        'share_url': request.build_absolute_uri()
    })

def download_trip_txt(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id, user=request.user)

    packing_items = trip.packing_items.all().order_by('is_packed', 'name')
    packing_text = "\n".join([
        f"- [{'x' if item.is_packed else ' '}] {item.name}" for item in packing_items
    ])

    content = f"""Trip Name: {trip.name}
Start Date: {trip.start_date}
End Date: {trip.end_date}

Packing List:
{packing_text}
"""

    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename="{trip.name}_details.txt"'
    return response

def shared_trip_view(request, share_token):
    trip = get_object_or_404(Trip, share_token=share_token, is_public=True)
    return render(request, 'trips/shared_trip_detail.html', {'trip': trip})

def public_trip_view(request, token):
    trip = get_object_or_404(Trip, share_token=token, is_public=True)
    return render(request, 'trips/public_trip.html', {'trip': trip})

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
    photo_url = None

    try:
        response = requests.get(
            'https://api.unsplash.com/search/photos',
            params={'query': trip.destination, 'per_page': 1, 'orientation': 'portrait'},
            headers={'Authorization': 'Client-ID gR0mr2UCMNC_f50G9cuFxHBR38lI0Wpfrxt2ZFhhfGA'}  # ← insert your key here
        )
        data = response.json()
        if data.get('results'):
            photo_url = data['results'][0]['urls']['regular']
    except Exception as e:
        print(f"Unsplash API error: {e}")

    try:
        recommendations = get_place_recommendations(trip.destination, trip.trip_type, max_results=3)
    except Exception as e:
        print(f"Google Places API error: {e}")

    return render(request, 'trips/trip_detail.html', {
        'trip': trip,
        'photo_url': photo_url,
        'recommendations': recommendations
    })

@login_required
def packing_list(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id, user=request.user)

    if not trip.packing_items.exists() and not trip.manually_cleared:
        generate_packing_list(trip)

    if request.method == 'POST':
        new_item = request.POST.get('new_item')
        if new_item:
            PackingItem.objects.create(trip=trip, name=new_item)
            if trip.manually_cleared:
                trip.manually_cleared = False
                trip.save()

    items = trip.packing_items.all().order_by('is_packed', 'name')
    return render(request, 'trips/packing_list.html', {'trip': trip, 'items': items})

@login_required
def update_packing_list(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id, user=request.user)

    if request.method == 'POST':
        # Delete selected item
        if 'delete_item' in request.POST:
            item_name = request.POST.get('delete_item')
            PackingItem.objects.filter(trip=trip, name=item_name).delete()

        # Mark items as packed
        packed_items = request.POST.getlist('packed_items')
        for item in trip.packing_items.all():
            item.is_packed = item.name in packed_items
            item.save()

        # If all items were deleted, mark trip as manually cleared
        if not trip.packing_items.exists():
            trip.manually_cleared = True
            trip.save()

    return redirect('packing_list', trip_id=trip.id)

@login_required
def leave_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            return redirect('profile')  # Or wherever you want
    else:
        form = FeedbackForm()
    return render(request, 'trips/leave_feedback.html', {'form': form})

@login_required
def toggle_public_trip(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id, user=request.user)
    trip.is_public = not trip.is_public
    trip.save()
    return redirect('trip_detail', trip_id=trip.id)