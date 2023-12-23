class AirQualitySensor:
    """
    Represents an air quality sensor device.
    """

    def __init__(self, device_id):
        """
        Initializes the AirQualitySensor object.

        Args:
            device_id (str): The unique identifier for the device.
        """

        self.device_id = device_id  # Store the device ID
        self.send_airquality_event_callback = None  # Callback to notify of events

    def set_send_airquality_event_callback(self, callback):
        """ Internal use"""
        self.send_airquality_event_callback = callback

    def send_airquality_event(self, pm1: int, pm2_5: int, pm10: int, cause="PHYSICAL_INTERACTION"):
        """
        Sends an air quality event notification.

        Args:
            pm1 (int): PM 1.0 concentration.
            pm2_5 (int): PM 2.5 concentration.
            pm10 (int): PM 10 concentration.
            cause (str, optional): The cause of the event (default: "PHYSICAL_INTERACTION").
        """

        if self.send_airquality_event_callback is not None:
            self.send_airquality_event_callback(self.device_id, pm1, pm2_5, pm10, cause)
