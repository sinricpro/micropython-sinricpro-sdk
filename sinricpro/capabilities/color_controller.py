class ColorController:
    """
    Represents a device that can control color.
    """

    def __init__(self, device_id):
        """
        Initializes the ColorController object.

        Args:
            device_id (str): The unique identifier for the device.
        """

        self.device_id = device_id  # Store the device ID
        self.on_color_callback = None  # Callback for color updates
        self.send_color_event_callback = None  # Callback to send color events

    def on_color(self, callback):
        """
        Sets a callback function to be invoked when the color changes.

        Args:
            callback (function): A function that takes the following arguments:
                - r (int): The red color component (0-255).
                - g (int): The green color component (0-255).
                - b (int): The blue color component (0-255).
        """

        self.on_color_callback = callback

    def set_send_color_event_callback(self, callback):
        """ Internal use"""
        self.send_color_event_callback = callback

    def send_color_event(self, r: int, g: int, b: int, cause="PHYSICAL_INTERACTION"):
        """
        Sends a color event notification.

        Args:
            r (int): The red color component (0-255).
            g (int): The green color component (0-255).
            b (int): The blue color component (0-255).
            cause (str, optional): The cause of the event (default: "PHYSICAL_INTERACTION").
        """

        if self.send_color_event_callback is not None:
            self.send_color_event_callback(self.device_id, r, g, b, cause)
