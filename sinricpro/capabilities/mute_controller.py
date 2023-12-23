class MuteController:
    """
    Represents a mute controller device within the SinricPro framework.
    """

    def __init__(self, device_id):
        """
        Initializes the MuteController object.

        Args:
            device_id (str): The unique identifier for the device in SinricPro.
        """

        self.device_id = device_id  # Store the device ID
        self.on_mute_callback = None  # Callback for mute state changes
        self.send_mute_event_callback = None  # Callback to send mute events

    def on_mute(self, callback):
        """
        Sets a callback function to be invoked when the mute state changes.

        Args:
            callback (function): A function that takes the following argument:
                - mute (bool): True if muted, False if unmuted.
        """

        self.on_mute_callback = callback

    def set_send_mute_event_callback(self, callback):
        """ Internal use"""
        self.send_mute_event_callback = callback

    def send_mute_event(self, mute: bool, cause="PHYSICAL_INTERACTION"):
        """
        Sends a mute event notification to SinricPro.

        Args:
            mute (bool): The new mute state (True for muted, False for unmuted).
            cause (str, optional): The cause of the event (default: "PHYSICAL_INTERACTION").
        """

        if self.send_mute_event_callback is not None:
            self.send_mute_event_callback(self.device_id, mute, cause)
