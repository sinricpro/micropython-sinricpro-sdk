class ContactSensor:
    """
    Represents a contact sensor device within the SinricPro SDK.
    """

    def __init__(self, device_id):
        """
        Initializes the ContactSensor object.

        Args:
            device_id (str): The unique identifier for the device in SinricPro.
        """

        self.device_id = device_id  # Store the device ID
        self.send_contact_event_callback = None  # Callback to send contact events

    def set_send_contact_event_callback(self, callback):
        """ Internal use"""
        self.send_contact_event_callback = callback

    def send_contact_event(self, detected: bool, cause="PHYSICAL_INTERACTION"):
        """
        Sends a contact event notification to SinricPro.

        Args:
            detected (bool): True if contact is detected, False otherwise.
            cause (str, optional): The cause of the event (default: "PHYSICAL_INTERACTION").
        """

        if self.send_contact_event_callback is not None:
            self.send_contact_event_callback(self.device_id, detected, cause)
