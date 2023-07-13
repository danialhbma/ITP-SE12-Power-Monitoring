from influxdb_client import Point
from abc import ABC, abstractmethod

class InfluxDBMeasurement(ABC):
    """
    Abstract base class for representing sensor readings or api data.
    Subclasses must implement the `set_tags` and `set_fields` methods to set the tags and fields for the sensor data.
    Tags and fields are required to create a Point data-type (measuremebt) which will be inserted into InfluxDB.
    """
    @abstractmethod
    def set_tags(self) -> dict:
        # Creates a dictionary that contains all tags to identify this reading
        # e.g., self.tags = {"device": "Light Sensor 2"}
        pass
    
    @abstractmethod
    def set_fields(self) -> dict:
        # Creates a dictionary that contains all fields i.e., readings for a measurement
        # e.g., self.fields = {"temp": your_temp_reading, "humidity", "your_humidity_reading"}
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

    def create_measurement(self) -> Point:
        # Returns a Point object, which represents the sensor / API data (a measurement) in InfluxDB 
        measurement = self._create_data_point(self.measurement_name, self.tags, self.fields)
        return measurement