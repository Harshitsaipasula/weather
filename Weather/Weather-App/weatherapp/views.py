from django.shortcuts import render
from django.contrib import messages
import requests
import datetime

def home(request):
    if 'city' in request.POST:
        city = request.POST['city']
    else:
        city = 'indore'

    
    WEATHER_API_KEY = 'e0fa745751123d43257390426f02a264'  
    GOOGLE_API_KEY = 'AIzaSyBJzo_DA2cVnEt9xD-nsTcyK91vhv_yXzY'       
    SEARCH_ENGINE_ID = '20cb31d8225704e8d' 

    # Weather API URL using city name (using 'q={city}' for city search)
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}'
    PARAMS = {'units': 'metric'}

    # Google Custom Search for city image
    query = city + " 1920x1080"
    page = 1
    start = (page - 1) * 10 + 1
    searchType = 'image'
    city_url = (
        f"https://www.googleapis.com/customsearch/v1"
        f"?key={GOOGLE_API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}"
        f"&start={start}&searchType={searchType}&imgSize=xlarge"
    )

    image_url = "https://images.pexels.com/photos/3408744/pexels-photo-3408744.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260"  # Default image
    try:
        image_response = requests.get(city_url)
        image_data = image_response.json()
        search_items = image_data.get("items")
        if search_items and len(search_items) >= 2:
            image_url = search_items[1]['link']
    except Exception:
        pass  # Keep default image if any error occurs

    try:
        # Make sure to print the response for debugging
        data = requests.get(url, params=PARAMS).json()
        print(f"API Response for {city}: {data}")  # Print for debugging
        
        # Check if the API response is valid
        if data.get("cod") != 200:
            raise ValueError("API returned error: " + data.get("message", "Unknown error"))

        description = data['weather'][0]['description']
        icon = data['weather'][0]['icon']
        temp = data['main']['temp']
        day = datetime.date.today()

        return render(request, 'weatherapp/index.html', {
            'description': description,
            'icon': icon,
            'temp': temp,
            'day': day,
            'city': city,
            'exception_occurred': False,
            'image_url': image_url
        })

    except ValueError as ve:
        print(f"Error: {ve}")
        exception_occurred = True
        messages.error(request, f"Error: {ve}")
        day = datetime.date.today()

        return render(request, 'weatherapp/index.html', {
            'description': 'clear sky',
            'icon': '01d',
            'temp': 25,
            'day': day,
            'city': city,
            'exception_occurred': exception_occurred,
            'image_url': image_url
        })
