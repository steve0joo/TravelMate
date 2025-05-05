# trips/utils.py

import requests
from datetime import date
from django.conf import settings
from .models import PackingItem


def generate_packing_list(trip):
    """
    Generates a packing list for the given trip.
    Includes base items, trip-type-specific items, and weather-driven extras.
    """
    # Skip generation if items already exist
    if trip.packing_items.exists():
        return

    # Base items everyone needs
    base_items = ['Toothbrush', 'Toothpaste', 'Socks', 'Underwear', 'Phone Charger']

    # Additional items based on trip type
    type_specific = {
        'beach':    ['Swimsuit', 'Flip‑flops', 'Beach towel', 'Sunglasses', 'Sunscreen'],
        'city':     ['Comfortable shoes', 'Map/Guidebook', 'Power bank', 'Day bag'],
        'hiking':   ['Hiking boots', 'Backpack', 'Water bottle', 'Trail snacks', 'First‑aid kit'],
        'business': ['Laptop', 'Business cards', 'Formal attire', 'Notebook', 'Pen'],
        'snow':     ['Winter coat', 'Gloves', 'Beanie', 'Snow boots', 'Ski pass'],
    }

    items = base_items + type_specific.get(trip.trip_type, [])

    # Weather-based extras via Open-Meteo
    try:
        # Geocode the destination
        resp_geo = requests.get(
            'https://geocoding-api.open-meteo.com/v1/search',
            params={'name': trip.destination, 'count': 1, 'language': 'en'},
            timeout=5
        )
        resp_geo.raise_for_status()
        geo_results = resp_geo.json().get('results')
        if geo_results:
            lat = geo_results[0]['latitude']
            lon = geo_results[0]['longitude']

            # Fetch daily forecast
            resp_fc = requests.get(
                'https://api.open-meteo.com/v1/forecast',
                params={
                    'latitude': lat,
                    'longitude': lon,
                    'daily': 'temperature_2m_max,weathercode',
                    'timezone': 'auto',
                },
                timeout=5
            )
            resp_fc.raise_for_status()
            daily = resp_fc.json().get('daily', {})

            dates = daily.get('time', [])
            tmaxs = daily.get('temperature_2m_max', [])
            codes = daily.get('weathercode', [])

            for d_str, tmax, code in zip(dates, tmaxs, codes):
                # Parse the ISO date string
                d = date.fromisoformat(d_str)
                # Only include days within the trip date range
                if not (trip.start_date <= d <= trip.end_date):
                    continue

                # Rain codes → add umbrella & rain jacket
                if code in [51,53,55,56,57,61,63,65,66,67,80,81,82]:
                    items += ['Umbrella', 'Rain jacket']
                # Snow codes → add warm boots & thermal socks
                if code in [71,73,75,77,85,86]:
                    items += ['Warm boots', 'Thermal socks']
                # Cold days → heavy coat & gloves
                if tmax < 5:
                    items += ['Heavy coat', 'Gloves']
                # Very hot days → sunscreen & sunhat
                if tmax > 30:
                    items += ['Sunscreen', 'Sunhat']
    except Exception:
        # Silently ignore weather failures
        pass

    # Deduplicate while preserving order
    unique_items = list(dict.fromkeys(items))

    # Save packing items
    for name in unique_items:
        PackingItem.objects.create(trip=trip, name=name)

def get_place_recommendations(destination, trip_type="other", max_results=3):
    # Map trip types to Google Places types
    trip_type_to_place_type = {
        "beach": "beach",
        "city": "tourist_attraction",
        "hiking": "park",
        "business": "coworking_space",
        "snow": "ski_resort",
        "other": "point_of_interest"
    }

    place_type = trip_type_to_place_type.get(trip_type, "point_of_interest")

    base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": f"{place_type} in {destination}",
        "key": {settings.GOOGLE_PLACES_API_KEY},
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    recommendations = []
    if data.get("results"):
        for place in data["results"][:max_results]:
            recommendations.append({
                "name": place.get("name"),
                "address": place.get("formatted_address"),
                "rating": place.get("rating"),
            })

    return recommendations