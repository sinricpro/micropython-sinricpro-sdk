class BrightnessController:
    """
    Represents a device that can control brightness.
    """

    def __init__(self, device_id):
        """
        Initializes the BrightnessController object.

        Args:
            device_id (str): The unique identifier for the device.
        """

        self.device_id = device_id  # Store the device ID
        self.on_brightness_callback = None  # Callback for brightness updates
        self.on_adjust_brightness_callback = None  # Callback for brightness adjustment requests
        self.send_brightness_event_callback = None  # Callback to send brightness events

    def on_brightness(self, callback):
        """
        Sets a callback function to be invoked when the brightness is updated.

        Args:
            callback (function): A function that takes the following arguments:
                - brightness (int): The new brightness value.
        """

        self.on_brightness_callback = callback

    def on_adjust_brightness(self, callback):
        """
        Sets a callback function to be invoked when a brightness adjustment request is received.

        Args:
            callback (function): A function that takes the following arguments:
                - brightness_delta (int): The amount to adjust the brightness (positive or negative).
        """

        self.on_adjust_brightness_callback = callback

    def set_send_brightness_event_callback(self, callback):
        """ Internal use"""
        self.send_brightness_event_callback = callback

    def send_brightness_event(self, brightness: int, cause="PHYSICAL_INTERACTION"):
        """
        Sends a brightness event notification.

        Args:
            brightness (int): The brightness value.
            cause (str, optional): The cause of the event (default: "PHYSICAL_INTERACTION").
        """

        if self.send_brightness_event_callback is not None:
            self.send_brightness_event_callback(self.device_id, brightness, cause)
