class MotionSensor:
    """
    Represents a motion sensor device within the SinricPro framework.
    """

    def __init__(self, device_id):
        """
        Initializes the MotionSensor object.

        Args:
            device_id (str): The unique identifier for the device in SinricPro.
        """

        self.device_id = device_id  # Store the device ID
        self.send_motion_event_callback = None  # Callback to send motion events

    def set_send_motion_event_callback(self, callback):
        """ Internal use"""
        self.send_motion_event_callback = callback

    def send_motion_event(self, detected: bool, cause="PHYSICAL_INTERACTION"):
        """
        Sends a motion event notification to SinricPro.

        Args:
            detected (bool): True if motion is detected, False otherwise.
            cause (str, optional): The cause of the event (default: "PHYSICAL_INTERACTION").
        """

        if self.send_motion_event_callback is not None:
            self.send_motion_event_callback(self.device_id, detected, cause)
