class EqualizerController:
    """
    Represents an equalizer device within the SinricPro framework.
    """

    def __init__(self, device_id: str):
        """
        Initializes the EqualizerController object.

        Args:
            device_id (str): The unique identifier for the device in SinricPro.
        """

        self.device_id = device_id  # Store the device ID
        self.on_set_bands_callback = None  # Callback for setting equalizer bands
        self.on_adjust_bands_callback = None  # Callback for adjusting equalizer bands
        self.on_reset_bands_callback = None  # Callback for resetting equalizer bands
        self.send_bands_event_callback = None  # Callback to send equalizer events

    def on_set_bands(self, callback):
        """
        Sets a callback function to be invoked when equalizer bands are set.

        Args:
            callback (function): A function that takes the following arguments:
                - bands (str): A string representation of the equalizer band levels (format depends on device implementation).
        """

        self.on_set_bands_callback = callback

    def on_adjust_bands(self, callback):
        """
        Sets a callback function to be invoked when equalizer bands are adjusted.

        Args:
            callback (function): A function that takes the following arguments:
                - bands (str): A string representation of the adjusted equalizer band levels (format depends on device implementation).
        """

        self.on_adjust_bands_callback = callback

    def on_reset_bands(self, callback):
        """
        Sets a callback function to be invoked when equalizer bands are reset.
        """

        self.on_reset_bands_callback = callback

    def set_send_bands_event_callback(self, callback):
        """ Internal use"""
        self.send_bands_event_callback = callback

    def send_bands_event(self, bands: str, level: int, cause="PHYSICAL_INTERACTION"):
        """
        Sends an equalizer event notification to SinricPro.

        Args:
            bands (str): A string representation of the affected equalizer bands.
            level (int): The level of the affected bands.
            cause (str, optional): The cause of the event (default: "PHYSICAL_INTERACTION").
        """

        if self.send_bands_event_callback is not None:
            self.send_bands_event_callback(self.device_id, bands, level, cause)
