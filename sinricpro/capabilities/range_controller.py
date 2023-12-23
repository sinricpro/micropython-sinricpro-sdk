class RangeController:
    """
    Represents a device that supports setting and adjusting range values within the SinricPro framework.
    """

    def __init__(self, device_id):
        """
        Initializes the RangeController object.

        Args:
            device_id (str): The unique identifier for the device in SinricPro.
        """

        self.device_id = device_id  # Store the device ID
        self.on_range_value_callback = None  # Callback for setting specific range values
        self.on_adjust_range_value_callback = None  # Callback for adjusting range values by a relative amount
        self.n_range_value_instances = {}  # Purpose unclear, likely for managing multiple range value instances

    def on_range_value(self, callback):
        """
        Sets a callback function to be invoked when a specific range value is set.

        Args:
            callback (function): A function that takes the following argument:
                - range_value (int or float): The new range value to be set.
        """

        self.on_range_value_callback = callback

    def on_adjust_range_value(self, callback):
        """
        Sets a callback function to be invoked when the range value is adjusted by a relative amount.

        Args:
            callback (function): A function that takes the following argument:
                - delta (int or float): The amount to adjust the range value by (positive or negative).
        """

        self.on_adjust_range_value_callback = callback

    def set_send_range_value_event_callback(self, callback):
        """ Internal use"""
        self.send_range_value_event_callback = callback

    def send_range_value_event(self, range_value, cause="PHYSICAL_INTERACTION"):
        """
        Sends a range value event notification to SinricPro.

        Args:
            range_value (int or float): The new range value.
            cause (str, optional): The cause of the event (default: "PHYSICAL_INTERACTION").
        """

        if self.send_range_value_event_callback is not None:
            self.send_range_value_event_callback(self.device_id, None, range_value, cause)  # Note: Instance is None
