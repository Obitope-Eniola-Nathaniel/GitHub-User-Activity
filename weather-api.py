import requests
import json
import redis
import os
from dotenv import load_dotenv

load_dotenv()

api = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/'
key = os.getenv('API_KEY')

# Connect to Redis Cloud
redis_client = redis.Redis(
    host="redis-18440.c84.us-east-1-2.ec2.redns.redis-cloud.com",
    port=18440,
    password="X3INdirCN59zu2IsuSGgDjGxTBImeJ3o",
    decode_responses=True  # Ensures strings are returned instead of bytes
)

# Test the connection
try:
    redis_client.ping()
    print("✅ Connected to Redis Cloud successfully!")
except redis.ConnectionError:
    print("❌ Failed to connect to Redis.")

def get_weather_api(city):
    # Define the API endpoint URL

    result = redis_client.get(city)
    if result:
        print('Data retrieved from Redis')
        return result
    else:
        url = api + f'{city}?unitGroup=us&key={key}&contentType=json'
        print('Data retrieved from API')
        try:
            # Make a GET request to the API endpoint using requests.get()
            response = requests.get(url)
        # Check if the request was successful (status code 200)
            if response.status_code == 200:
                posts = response.json()
                redis_client.setex(city, 43200, str(posts))
                
                return posts
            else:
                print('Error:', response.status_code)
                return None
        except requests.exceptions.RequestException as e:
        # Handle any network-related errors or exceptions
            print('Error:', e)
            return None


weather = get_weather_api('New York')
print(json.dumps(weather, indent=2))
# print(weather['days'][0]['tempmax'])





