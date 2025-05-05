# TravelMate
## CS 2340 (Object and Design) Final Project

This website is built using Django Web Framework.

TravelMate is a web application that helps users plan trips more easily by providing suggestions for what to wear based on weather forecasts and activities at their destination. The app creates packing lists automatically, offers local travel tips, and lets users save and manage their travel plans. It integrates features like weather forecasts from OpenWeather API, location recommendations via Google Places API, and PackPoint API to help generate packing lists.

TravelMate's main goal is to help users feel well-prepared for their trips by reducing the stress of
planning and packing. Users will be able to check local weather, get outfit suggestions, and
customize packing lists, making their travel experience smoother and more enjoyable.

### 1. Installation for .env

```
$ touch .env
```

### 2. Add all required keys on .env

```
$ SECRET_KEY=your_django_secret_key_here
$ VISUAL_CROSSING_API_KEY=your_api_key_here
$ EMAIL_HOST_PASSWORD=your_email_password_here
$ UNSPLASH_API_KEY=your_api_key_here
$ GOOGLE_PLACES_API_KEY=your_api_key_here
$ OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Create and activate a virtual environment
```
$ python3 -m venv venv
$ source venv/bin/activate
```

### 4. Install dependencies
```
$ pip install -r requirements.txt
```

### 5. Run the server
```
$ python manage.py runserver
```

#### Contributers
@steve0joo

@DavidymLee

@IronhawkReigns

@JackWachter

@philharmoniic
