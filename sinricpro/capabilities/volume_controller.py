class VolumeController:
    """
    Represents a device with volume control within the SinricPro framework.
    """

    def __init__(self, device_id):
        """
        Initializes the VolumeController object.

        Args:
            device_id (str): The unique identifier for the device in SinricPro.
        """

        self.device_id = device_id  # Store the device ID
        self.on_set_volume_callback = None  # Callback for setting specific volume values
        self.on_adjust_volume_callback = None  # Callback for adjusting volume by a relative amount

    def on_set_volume(self, callback):
        """
        Sets a callback function to be invoked when a specific volume value is set.

        Args:
            callback (function): A function that takes the following argument:
                - volume (int): The new volume value to be set.
        """

        self.on_set_volume_callback = callback

    def on_adjust_volume(self, callback):
        """
        Sets a callback function to be invoked when the volume is adjusted by a relative amount.

        Args:
            callback (function): A function that takes the following argument:
                - delta (int): The amount to adjust the volume by (positive or negative).
        """

        self.on_adjust_volume_callback = callback

    def set_send_volume_event(self, callback):
        """ Internal use"""
        self.send_volume_event_callback = callback

    def send_volume_event(self, volume: int, cause="PHYSICAL_INTERACTION"):
        """
        Sends a volume event notification to SinricPro.

        Args:
            volume (int): The new volume value.
            cause (str, optional): The cause of the event (default: "PHYSICAL_INTERACTION").
        """

        if self.send_volume_event_callback is not None:
            self.send_volume_event_callback(self.device_id, volume, cause)
