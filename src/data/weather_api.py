import requests
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.config import WEATHER_API_KEY

def get_weather(venue_name):
    """
    Fetches real-time weather data for a given stadium/venue using OpenWeatherMap.
    Falls back to mock data if API key is invalid or request fails.
    """
    STADIUM_TO_CITY = {
        'Wankhede': 'Mumbai',
        'Eden Gardens': 'Kolkata',
        'Chinnaswamy': 'Bengaluru',
        'Chepauk': 'Chennai',
        'Narendra Modi Stadium': 'Ahmedabad',
        'Rajiv Gandhi Stadium': 'Hyderabad',
        'Arun Jaitley Stadium': 'Delhi'
    }
    
    city_name = STADIUM_TO_CITY.get(venue_name, 'Mumbai') # Fallback to Mumbai
    
    # Mock fallback
    if not WEATHER_API_KEY or WEATHER_API_KEY == "dummy_weather_api_key":
        print(f"[Weather API] Using mock data for {city_name} (No API Key)")
        import random
        return {
            "temp": round(random.uniform(25.0, 38.0), 1), 
            "humidity": random.randint(40, 90), 
            "condition": random.choice(["Clear", "Cloudy", "Rain Probable"])
        }
        
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={WEATHER_API_KEY}&units=metric"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                "temp": data['main']['temp'],
                "humidity": data['main']['humidity'],
                "condition": data['weather'][0]['main']
            }
        else:
            print(f"[Weather API] Warning: API returned {response.status_code}. Using mock fallback.")
            return {"temp": 30.0, "humidity": 50, "condition": "Clear"}
    except Exception as e:
        print(f"[Weather API] Error fetching weather: {e}. Using mock fallback.")
        return {"temp": 30.0, "humidity": 50, "condition": "Clear"}

if __name__ == "__main__":
    print(get_weather("Mumbai"))
