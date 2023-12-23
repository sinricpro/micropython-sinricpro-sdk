class PowerStateController:
    """
    Represents a device that supports power state control within the SinricPro framework.
    """

    def __init__(self, device_id):
        """
        Initializes the PowerStateController object.

        Args:
            device_id (str): The unique identifier for the device in SinricPro.
        """

        self.device_id = device_id  # Store the device ID
        self.power_state_callback = None  # Callback for power state changes
        self.send_power_state_event_callback = None  # Callback to send power state events

    def on_power_state(self, callback):
        """
        Sets a callback function to be invoked when the power state changes.

        Args:
            callback (function): A function that takes the following argument:
                - state (bool): True if the device is on, False if it's off.
        """

        self.power_state_callback = callback

    def set_send_power_state_event_callback(self, callback):
        """ Internal use"""
        self.send_power_state_event_callback = callback

    def send_power_state_event(self, state: bool, cause="PHYSICAL_INTERACTION"):
        """
        Sends a power state event notification to SinricPro.

        Args:
            state (bool): The new power state (True for on, False for off).
            cause (str, optional): The cause of the event (default: "PHYSICAL_INTERACTION").
        """

        self.send_power_state_event_callback(self.device_id, state, cause)
