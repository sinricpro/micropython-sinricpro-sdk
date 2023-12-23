class MediaController:
    """
    Represents a media controller device within the SinricPro framework.
    """

    def __init__(self, device_id):
        """
        Initializes the MediaController object.

        Args:
            device_id (str): The unique identifier for the device in SinricPro.
        """

        self.device_id = device_id  # Store the device ID
        self.on_media_control_callback = None  # Callback for media control commands
        self.send_media_control_event_callback = None  # Callback to send media control events

    def on_media_control(self, callback):
        """
        Sets a callback function to be invoked when media control commands are received.

        Args:
            callback (function): A function that takes the following argument:
                - media_control (str): The media control command (e.g., "Play", "Pause", "Next").
        """

        self.on_media_control_callback = callback

    def set_send_media_control_event_callback(self, callback):
        """ Internal use"""
        self.send_media_control_event_callback = callback

    def send_media_control_event(self, media_control: str, cause="PHYSICAL_INTERACTION"):
        """
        Sends a media control event notification to SinricPro.

        Args:
            media_control (str): The media control command that triggered the event.
            cause (str, optional): The cause of the event (default: "PHYSICAL_INTERACTION").
        """

        if self.send_media_control_event_callback is not None:
            self.send_media_control_event_callback(self.device_id, media_control, cause)
