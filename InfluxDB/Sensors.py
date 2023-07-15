from influxdb_client import Point
from abc import ABC, abstractmethod
from InfluxDBMeasurement import InfluxDBMeasurement

class SGP30SensorData(InfluxDBMeasurement):
    """Class for TVOC/CO2 SGP30 Sensor Readings - tvoc and co2
       > TVOC stands for Total Volatile Organic Compounds.
    """
    def __init__(self, co2=0):
        self.co2 = co2
        self.measurement_name = "air_quality"
        self.tags = self.set_tags()
        self.fields = self.set_fields()
    
    def set_tags(self):
        return {"device": "TVOC/eCO2 Gas Sensor Unit (SGP30)"}
    
    def set_fields(self):
        return {"co2": self.co2}
    
class ENVHatSensorData(InfluxDBMeasurement):
    """Class for ENV Hat Sensor data - temp, humidity, air pressure and mag field."""
    def __init__(self, temperature=0, humidity=0):
        self.temperature = temperature
        self.humidity = humidity
        self.measurement_name = "enviromental_quality"
        self.tags = self.set_tags()
        self.fields = self.set_fields()
    
    def set_tags(self):
        return {"device": "ENV Hat (DHT12, BMP280, BMM150)"}
    
    def set_fields(self):
        return {"temperature": self.temperature, "humidity": self.humidity}

class GrowLightsPowerUsageSensor(InfluxDBMeasurement):
    """Class for Growlight Power Usage Sensor."""
    def __init__(self, wattage=0):
        self.wattage = wattage
        self.measurement_name = "growlight_power_consumption"
        self.tags = self.set_tags()
        self.fields = self.set_fields()
    
    def set_tags(self):
        return {"device": "Tuya Power"}
    
    def set_fields(self):
        return {"wattage": self.wattage}

class AirconPowerUsageSensor(InfluxDBMeasurement):
    def __init__(self, wattage=0):
        self.wattage = wattage
        self.measurement_name = "aircon_power_consumption"
        self.tags = self.set_tags()
        self.fields = self.set_fields()
    
    def set_tags(self):
        return {"device": "Clip On Voltmeter"}
    
    def set_fields(self):
        return {"wattage": self.wattage}

