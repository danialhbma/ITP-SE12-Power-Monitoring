import requests
import sys 
# Allows up to 1000 requests per day for free

# Replace 'YOUR_API_KEY' with your OpenWeatherMap API key
api_key = '4e562538a0f07b5faa5d3ca57d46f8dc'

# Set the coordinates for Republic Polytechnic (RP) in Singapore
latitude = 1.4462237543825216
longitude =  103.78469667962912

# Make the API request
url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}&units=metric"
response = requests.get(url)
data = response.json()
print(data)

# Extract temperature from the response
temperature = data['main']['temp']

# Print the temperature
print(f"Temperature at Republic Polytechnic (RP): {temperature} °C")
