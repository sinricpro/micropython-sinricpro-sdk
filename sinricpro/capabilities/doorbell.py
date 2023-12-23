class Doorbell:
    """
    Represents a doorbell device within the SinricPro framework.
    """

    def __init__(self, device_id):
        """
        Initializes the Doorbell object.

        Args:
            device_id (str): The unique identifier for the device in SinricPro.
        """

        self.device_id = device_id  # Store the device ID
        self.send_doorbell_event_callback = None  # Callback to send doorbell events

    def set_send_doorbell_event_callback(self, callback):
        """ Internal use"""
        self.send_doorbell_event_callback = callback

    def send_doorbell_event(self, cause="PHYSICAL_INTERACTION"):
        """
        Sends a doorbell event notification to SinricPro.

        Args:
            cause (str, optional): The cause of the event (default: "PHYSICAL_INTERACTION").
        """

        if self.send_doorbell_event_callback is not None:
            self.send_doorbell_event_callback(self.device_id, cause)
