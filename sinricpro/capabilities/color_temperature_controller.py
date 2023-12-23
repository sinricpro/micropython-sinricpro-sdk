class ColorTemperatureController:
    """
    Represents a device that can control color temperature.
    """

    def __init__(self, device_id):
        """
        Initializes the ColorTemperatureController object.

        Args:
            device_id (str): The unique identifier for the device.
        """

        self.device_id = device_id  # Store the device ID
        self.on_color_temperature_callback = None  # Callback for color temperature updates
        self.on_increase_color_temperature_callback = None  # Callback for increasing color temperature
        self.on_decrease_color_temperature = None  # Callback for decreasing color temperature
        self.send_color_temperature_event_callback = None  # Callback to send color temperature events

    def on_color_temperature(self, callback):
        """
        Sets a callback function to be invoked when the color temperature changes.

        Args:
            callback (function): A function that takes the following arguments:
                - color_temperature (int): The color temperature value.
        """

        self.on_color_temperature_callback = callback

    def on_increase_color_temperature(self, callback):
        """
        Sets a callback function to be invoked when a request to increase color temperature is received.

        Args:
            callback (function): A function that takes no arguments.
        """

        self.on_increase_color_temperature_callback = callback

    def on_decrease_color_temperature(self, callback):
        """
        Sets a callback function to be invoked when a request to decrease color temperature is received.

        Args:
            callback (function): A function that takes no arguments.
        """

        self.on_decrease_color_temperature_callback = callback

    def set_send_color_temperature_event_callback(self, callback):
        """ Internal use"""
        self.send_color_temperature_event_callback = callback

    def send_color_temperature_event(self, color_temperature: int, cause="PHYSICAL_INTERACTION"):
        """
        Sends a color temperature event.

        Args:
            color_temperature (int): The color temperature value.
            cause (str, optional): The cause of the event (default: "PHYSICAL_INTERACTION").
        """

        if self.send_color_temperature_event_callback is not None:
            self.send_color_temperature_event_callback(self.device_id, color_temperature, cause)
