class TemperatureSensor:
    """
    Represents a temperature sensor device within the SinricPro framework.
    """

    def __init__(self, device_id):
        """
        Initializes the TemperatureSensor object.

        Args:
            device_id (str): The unique identifier for the device in SinricPro.
        """

        self.device_id = device_id  # Store the device ID
        self.send_temperature_event_callback = None  # Callback for sending temperature events

    def set_send_temperature_event_callback(self, callback):
        """ Internal use"""
        self.send_temperature_event_callback = callback

    def send_temperature_event(self, temperature: float, humidity: float = -1, cause="PERIODIC_POLL"):
        """
        Sends a temperature event notification to SinricPro.

        Args:
            temperature (float): The measured temperature.
            humidity (float, optional): The measured humidity (default: -1.0 if not available).
            cause (str, optional): The cause of the event (default: "PERIODIC_POLL").
        """

        if self.send_temperature_event_callback is not None:
            self.send_temperature_event_callback(self.device_id, temperature, humidity, cause)
