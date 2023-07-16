import requests
from InfluxDBMeasurement import InfluxDBMeasurement
from InfluxDBWriter import InfluxDBWriter

class OpenWeatherMapAPIClient(InfluxDBMeasurement): 
    """ Handles API calls to OpenWeatherMap """
    def __init__(self, latitude, longitude):
        self.api_key = '4e562538a0f07b5faa5d3ca57d46f8dc' # change to os.environ variable
        self.latitude = latitude
        self.longitude = longitude
        self.measurement_name = "External Weather Conditions"
        self.fields = {} 
        self.tags = {} 

    def set_latitude(self, latitude):
        self.latitude = latitude
    
    def set_longitude(self, longitude):
        self.longitude = longitude

    def get_weather_information(self):
        """Makes an API call to retrieve weather information, collected data is converted into fields to be written to influx db"""
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={self.latitude}&lon={self.longitude}&appid={self.api_key}&units=metric"
        response = requests.get(url)
        self.data = response.json()
        self.set_fields()
        self.set_tags()

    def set_fields(self):
        self.fields = {
            'weather_main': self.data.get('weather', [{}])[0].get('main'),
            'temperature': self.data.get('main', {}).get('temp'),
            'feels_like': self.data.get('main', {}).get('feels_like'),
            'pressure': self.data.get('main', {}).get('pressure'),
            'humidity': self.data.get('main', {}).get('humidity'),
            'temp_min': self.data.get('main', {}).get('temp_min'),
            'temp_max': self.data.get('main', {}).get('temp_max'),
            'wind_speed': self.data.get('wind', {}).get('speed'),
            'wind_deg': self.data.get('wind', {}).get('deg'),
            'cloudiness': self.data.get('clouds', {}).get('all'),
         }
        print(self.fields)

    def set_tags(self):
        self.tags = {"source": "OpenWeatherMap", "location": self.data["name"]}

open_weather_client = OpenWeatherMapAPIClient(latitude = 1.4462237543825216, longitude =  103.78469667962912)
open_weather_client.get_weather_information()
writer = InfluxDBWriter("WeatherAPI")
writer.write_single_measurement(open_weather_client.create_measurement())
