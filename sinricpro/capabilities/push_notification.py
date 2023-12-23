class PushNotificationController:
    """
    Represents a device that supports sending push notifications within the SinricPro framework.
    """

    def __init__(self, device_id):
        """
        Initializes the PushNotificationController object.

        Args:
            device_id (str): The unique identifier for the device in SinricPro.
        """

        self.device_id = device_id  # Store the device ID
        self.send_push_notification_event_callback = None  # Callback to send push notification events

    def set_send_push_notification_event_callback(self, callback):
        """ Internal use"""
        self.send_push_notification_event_callback = callback

    def send_push_notification(self, notification: str, cause="PHYSICAL_INTERACTION"):
        """
        Sends a push notification event notification to SinricPro.

        Args:
            notification (str): The notification message to be sent.
            cause (str, optional): The cause of the event (default: "PHYSICAL_INTERACTION").
        """

        if self.send_push_notification_event_callback is not None:
            self.send_push_notification_event_callback(self.device_id, notification, cause)
