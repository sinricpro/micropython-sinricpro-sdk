class PercentageController:
    """
    Represents a device that supports percentage-based control within the SinricPro framework.
    """

    def __init__(self, device_id):
        """
        Initializes the PercentageController object.

        Args:
            device_id (str): The unique identifier for the device in SinricPro.
        """

        self.device_id = device_id  # Store the device ID
        self.on_set_percentage_callback = None  # Callback for setting a specific percentage
        self.on_adjust_percentage_callback = None  # Callback for adjusting the percentage by a relative amount
        self.send_set_percentage_event_callback = None  # Callback to send percentage events

    def on_set_percentage(self, callback):
        """ Internal use"""
        self.on_set_percentage_callback = callback

    def on_adjust_percentage(self, callback):
        """
        Sets a callback function to be invoked when the percentage is adjusted by a relative amount.

        Args:
            callback (function): A function that takes the following argument:
                - delta (int): The amount to adjust the percentage by (positive or negative).
        """

        self.on_adjust_percentage_callback = callback

    def set_send_set_percentage_event_callback(self, callback):
        """
        Sets a callback function to be invoked when percentage events should be sent.

        Args:
            callback (function): A function that takes the following arguments:
                - device_id (str): The device ID.
                - percentage (int): The percentage value that triggered the event.
                - cause (str, optional): The cause of the event (default: "PHYSICAL_INTERACTION").
        """

        self.send_set_percentage_event_callback = callback

    def send_set_percentage_event(self, percentage: int, cause="PHYSICAL_INTERACTION"):
        """
        Sends a percentage event notification to SinricPro.

        Args:
            percentage (int): The percentage value that triggered the event.
            cause (str, optional): The cause of the event (default: "PHYSICAL_INTERACTION").
        """

        if self.send_set_percentage_event_callback is not None:
            self.send_set_percentage_event_callback(self.device_id, percentage, cause)
