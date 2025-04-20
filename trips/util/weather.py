import requests

# --- Geocoding via Open‑Meteo ---
def geocode(city_name):
    """
    Uses Open‑Meteo’s free geocoding endpoint to get lat/lon.
    """
    url = 'https://geocoding-api.open-meteo.com/v1/search'
    params = {
        'name': city_name,
        'count': 1,
        'language': 'en',
    }
    resp = requests.get(url, params=params, timeout=5)
    resp.raise_for_status()
    data = resp.json().get('results')
    if not data:
        return None, None
    return data[0]['latitude'], data[0]['longitude']


# --- Fetch 7‑day daily forecast ---
def fetch_forecast(lat, lon):
    """
    Fetches daily max/min temps and weather codes for the next 7 days.
    """
    url = 'https://api.open-meteo.com/v1/forecast'
    params = {
        'latitude': lat,
        'longitude': lon,
        'daily': 'temperature_2m_max,temperature_2m_min,weathercode',
        'timezone': 'auto',
    }
    resp = requests.get(url, params=params, timeout=5)
    resp.raise_for_status()
    return resp.json()


# --- Map weather codes to human descriptions ---
def code_to_description(code):
    mapping = {
        0: 'Clear sky',
        1: 'Mainly clear',
        2: 'Partly cloudy',
        3: 'Overcast',
        45: 'Fog',
        48: 'Depositing rime fog',
        51: 'Light drizzle',
        53: 'Moderate drizzle',
        55: 'Dense drizzle',
        56: 'Freezing drizzle',
        57: 'Dense freezing drizzle',
        61: 'Light rain',
        63: 'Moderate rain',
        65: 'Heavy rain',
        66: 'Light freezing rain',
        67: 'Heavy freezing rain',
        71: 'Light snow',
        73: 'Moderate snow',
        75: 'Heavy snow',
        77: 'Snow grains',
        80: 'Light rain showers',
        81: 'Moderate rain showers',
        82: 'Violent rain showers',
        85: 'Light snow showers',
        86: 'Heavy snow showers',
        95: 'Thunderstorm',
        96: 'Thunderstorm with hail',
        99: 'Heavy hailstorm',
    }
    return mapping.get(code, 'Unknown')


# --- Outfit suggestion logic unchanged ---
def suggest_outfit(temp_c):
    if temp_c < 5:
        return 'Heavy coat, gloves & scarf'
    if temp_c < 15:
        return 'Jacket or warm sweater'
    if temp_c < 25:
        return 'Long‑sleeve shirt or light jacket'
    return 'T‑shirt & shorts'
