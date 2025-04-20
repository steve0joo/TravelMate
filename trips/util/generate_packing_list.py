
from datetime import date
from .weather import geocode, fetch_forecast
from trips.models import PackingItem

def generate_packing_list(trip):
    # don’t overwrite an existing list
    if trip.packing_items.exists():
        return

    # 1) Base + trip‑type items
    base_items = ['Toothbrush', 'Toothpaste', 'Socks', 'Underwear', 'Phone Charger']
    type_specific = {
        'beach':    ['Swimsuit', 'Flip‑flops', 'Beach towel', 'Sunglasses', 'Sunscreen'],
        'city':     ['Comfortable shoes', 'Map/Guidebook', 'Power bank', 'Day bag'],
        'hiking':   ['Hiking boots', 'Backpack', 'Water bottle', 'Trail snacks', 'First‑aid kit'],
        'business': ['Laptop', 'Business cards', 'Formal attire', 'Notebook', 'Pen'],
        'snow':     ['Winter coat', 'Gloves', 'Beanie', 'Snow boots', 'Ski pass'],
    }
    items = base_items + type_specific.get(trip.trip_type, [])

    # 2) Weather items
    try:
        lat, lon = geocode(trip.destination)
        if lat is not None:
            data = fetch_forecast(lat, lon)
            daily = data.get('daily', {})
            for d_str, tmax, code in zip(
                    daily.get('time', []),
                    daily.get('temperature_2m_max', []),
                    daily.get('weathercode', []),
                ):
                d = date.fromisoformat(d_str)
                if not (trip.start_date <= d <= trip.end_date):
                    continue

                # Rain codes → umbrella & rain jacket
                if code in [51,53,55,56,57,61,63,65,66,67,80,81,82]:
                    items += ['Umbrella', 'Rain jacket']
                # Snow codes → warm boots, thermal socks
                if code in [71,73,75,77,85,86]:
                    items += ['Warm boots', 'Thermal socks']
                # Cold days → heavy coat, gloves
                if tmax < 5:
                    items += ['Heavy coat', 'Gloves']
                # Hot days → sunscreen, sunhat
                if tmax > 30:
                    items += ['Sunscreen', 'Sunhat']
    except Exception:
        # silently ignore weather failures
        pass

    # 3) Dedupe & save
    for name in dict.fromkeys(items):
        PackingItem.objects.create(trip=trip, name=name)