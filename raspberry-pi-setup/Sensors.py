from influxdb_client import Point
from abc import ABC, abstractmethod

class SensorData(ABC):
    """
    Abstract base class for representing sensor measurements/readings. 
    Subclasses must implement the `set_tags` and `set_fields` methods to set the tags and fields for the sensor data.
    Tags and fields are required to create a Point data-type which will be inserted into InfluxDB.
    """
    @abstractmethod
    def set_tags(self) -> dict:
        # Creates a dictionary that contains all tags to identify this reading
        pass
    
    @abstractmethod
    def set_fields(self) -> dict:
        # Creates a dictionary that contains all fields i.e., readings for a measurement
        pass
    
    def _create_data_point(self, measurement_name, tags, fields):
        # Creates an InfluxDB measurement with the given name and adds the provided tags and fields. 
        # Returns a point that can be written to the InfluxDB bucket.
        point = Point(measurement_name)
        for tag, value in tags.items():
            point.tag(tag, value)
        for field, value in fields.items():
            point.field(field, value)
        return point

    def create_sensor_data(self) -> Point:
        # Returns a Point object, which represents the sensor data (a measurement) in InfluxDB 
        sensor_data = self._create_data_point(self.measurement_name, self.tags, self.fields)
        return sensor_data

class SGP30SensorData(SensorData):
    """Class for TVOC/CO2 SGP30 Sensor Readings - tvoc and co2
       > TVOC stands for Total Volatile Organic Compounds.
    """
    def __init__(self, tvoc, co2):
        self.tvoc = tvoc
        self.co2 = co2
        self.measurement_name = "air_quality"
        self.tags = self.set_tags()
        self.fields = self.set_fields()
    
    def set_tags(self):
        return {"device": "TVOC/eCO2 Gas Sensor Unit (SGP30)"}
    
    def set_fields(self):
        return {"tvoc": self.tvoc, "co2": self.co2}
    
class ENVHatSensorData(SensorData):
    """Class for ENV Hat Sensor data - temp, humidity, air pressure and mag field."""
    def __init__(self, temperature, humidity, air_pressure, mag_field):
        self.temperature = temperature
        self.humidity = humidity
        self.air_pressure = air_pressure
        self.mag_field = mag_field
        self.measurement_name = "enviromental_quality"
        self.tags = self.set_tags()
        self.fields = self.set_fields()
    
    def set_tags(self):
        return {"device": "ENV Hat (DHT12, BMP280, BMM150)"}
    
    def set_fields(self):
        return {"temperature": self.temperature, "humidity": self.humidity, "air_pressure": self.air_pressure, "mag_field": self.mag_field}

class GrowLightsPowerUsageSensor(SensorData):
    """Class for Growlight Power Usage Sensor."""
    def __init__(self, wattage):
        self.wattage = wattage
        self.measurement_name = "power_consumption"
        self.tags = self.set_tags()
        self.fields = self.set_fields()
    
    def set_tags(self):
        return {"device": "Tuya Power"}
    
    def set_fields(self):
        return {"wattage": self.wattage}

class AirconPowerUsageSensor(SensorData):
    def __init__(self, wattage):
        self.wattage = wattage
        self.measurement_name = "power_consumption"
        self.tags = self.set_tags()
        self.fields = self.set_fields()
    
    def set_tags(self):
        return {"device": "Clip On Voltmeter"}
    
    def set_fields(self):
        return {"wattage": self.wattage}

