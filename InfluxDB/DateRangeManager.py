from datetime import datetime, timedelta, timezone
import re

class DateRangeManager:
    """Helper class used to manage datetime objects i.e., datetime validation and datetime window used in InfluxDB queries"""
    def __init__(self):
        pass

    def _is_datetime(self, dt: datetime) -> bool:
        """Check if function parameter is a valid datetime object in ISO format"""
        try:
            # Check if the datetime string matches the ISO format pattern
            datetime.fromisoformat(dt)
            return True
        except (AttributeError, ValueError, TypeError):
            return False
    
    def validate_date_range(self, start: datetime, end: datetime):
        """Raises a ValueError if the date range is not valid for building a Flux query"""
        if not self._is_datetime(start) or not self._is_datetime(end):
            raise ValueError(f"Invalid date range: start [{start}] and end [{end}] dates must be valid datetime objects")
        if start >= end:
            raise ValueError(f"Invalid date range: start date [{start}] must be before end [{end}] date")

    def validate_aggregate_window(self, aggregate_window):
        """Raises a ValueError if aggregate window is not valid for building a Flux query"""
        if not self.is_valid_window(aggregate_window):
            raise ValueError(f"Invalid aggregate window provided - [{aggregate_window}]. Please use a valid format like '30d', '1h', '1w', etc.")
    
    def is_valid_window(self, window) -> bool:
        """Validates the time window format.Can be used to validated aggregate windows or time range.
        Args:
            window (str): The time window format to validate.
        Returns:
            bool: True if the format is valid, False otherwise.
        Valid Format:
            str: that follows {int}{s,m,h,d,w} e.g., valid formats 30s (30 seconds), 30m (30 minutes), 24h (24 hour) or 1d (1 day) 
        """
        match = re.match(r"(\d+)([dhmws])", window)
        return bool(match)

    def _parse_window(self, window:str) -> timedelta:
        """Parses and validates the time window format and returns the corresponding timedelta value.
        Args:
            window (str): The time window format. Examples: '1d', '3h', '30m', '1w', '60s'.
        Returns:
            timedelta: The timedelta value representing the duration of the time window.
        Raises:
            ValueError: If the window format is invalid.
        """
        if not self.is_valid_window(window.lower()):
            raise ValueError(f"Invalid window provided - [{window}]. Please use a valid format like '30d', '1h', '1w', etc.")

        match = re.match(r"(\d+)([dhmws])", window.lower())
        duration = int(match.group(1))
        unit = match.group(2)
        if unit == 'd':
            return timedelta(days=duration)
        elif unit == 'h':
            return timedelta(hours=duration)
        elif unit == 'm':
            return timedelta(minutes=duration)
        elif unit == 'w':
            return timedelta(weeks=duration)
        elif unit == 's':
            return timedelta(seconds=duration)
        
    def get_time_range(self, window):
        """Creates the start and end time ranges for InfluxDB queries, end time will always be the current time"""
        try:
            time_delta = self._parse_window(window)
            start_time = datetime.now(timezone.utc) - time_delta
            end_time = datetime.now(timezone.utc)
            return start_time.isoformat(), end_time.isoformat()
        except ValueError as e:
            print(f"Error creating time range: {e}")
            return None, None
        
    def nearest_hour(self, datetime_obj):
        nearest_hour = datetime_obj.replace(minute = 0, second = 0, microsecond = 0)
        print(nearest_hour.isoformat())



def main():
    drm = DateRangeManager()
    print("{:<35} {}".format("start", "end")) # Formating of start and end headers
    print(drm.get_time_range("5s")) # 5 sec interval 
    print(drm.get_time_range("30m")) #30 min interval
    print(drm.get_time_range("24h")) # 1d interval
    print(drm.get_time_range("30d")) # 30d 
    print(drm.get_time_range("abch")) # invalid 
    print(drm.get_time_range("1f")) # invalid - 'f' not accepted unit
    print(drm.get_time_range("0.0d")) # invalid - floats not accepted 
    print(drm.get_time_range("-2d")) # invalid - negative

if __name__ == "__main__":
    main()