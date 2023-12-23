class PowerLevelController:
    """
    Represents a device that supports power level control within the SinricPro framework.
    """

    def __init__(self, device_id):
        """
        Initializes the PowerLevelController object.

        Args:
            device_id (str): The unique identifier for the device in SinricPro.
        """

        self.device_id = device_id  # Store the device ID
        self.on_power_level_callback = None  # Callback for setting a specific power level
        self.on_adjust_power_level_callback = None  # Callback for adjusting the power level by a relative amount
        self.send_power_level_event_callback = None  # Callback to send power level events

    def on_power_level(self, callback):
        """
        Sets a callback function to be invoked when a specific power level is set.

        Args:
            callback (function): A function that takes the following argument:
                - power_level (int): The power level value to be set.
        """

        self.on_power_level_callback = callback

    def on_adjust_power_level(self, callback):
        """
        Sets a callback function to be invoked when the power level is adjusted by a relative amount.

        Args:
            callback (function): A function that takes the following argument:
                - delta (int): The amount to adjust the power level by (positive or negative).
        """

        self.on_adjust_power_level_callback = callback

    def set_send_power_level_event_callback(self, callback):
        """ Internal use"""
        self.send_power_level_event_callback = callback

    def send_power_level_event(self, power_level: int, cause="PHYSICAL_INTERACTION"):
        """
        Sends a power level event notification to SinricPro.

        Args:
            power_level (int): The power level value that triggered the event.
            cause (str, optional): The cause of the event (default: "PHYSICAL_INTERACTION").
        """

        if self.send_power_level_event_callback is not None:
            self.send_power_level_event_callback(self.device_id, power_level, cause)
