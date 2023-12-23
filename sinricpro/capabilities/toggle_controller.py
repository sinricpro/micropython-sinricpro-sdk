class ToggleController:
    """
    Represents a device with a toggleable state (on/off) within the SinricPro framework.
    """

    def __init__(self, device_id):
        """
        Initializes the ToggleController object.

        Args:
            device_id (str): The unique identifier for the device in SinricPro.
        """

        self.device_id = device_id  # Store the device ID
        self.on_toggle_state_callback = None  # Callback for toggle state changes

    def on_toggle_state(self, callback):
        """
        Sets a callback function to be invoked when the toggle state changes.

        Args:
            callback (function): A function that takes the following arguments:
                - state (bool): The new toggle state (True for on, False for off).
        """

        self.on_toggle_state_callback = callback

    def set_send_toggle_state_event_callback(self, callback):
        """ Internal use"""
        self.send_toggle_state_event_callback = callback

    def send_toggle_state_event(self, instance: str, state: bool, cause="PHYSICAL_INTERACTION"):
        """
        Sends a toggle state event notification to SinricPro.

        Args:
            instance (str): An instance name (for devices with multiple toggles).
            state (bool): The new toggle state.
            cause (str, optional): The cause of the event (default: "PHYSICAL_INTERACTION").
        """

        if self.send_toggle_state_event_callback is not None:
            self.send_toggle_state_event_callback(self.device_id, instance, state, cause)
