class PushNotificationController:
    def __init__(self, device_id):
        self.device_id = device_id
        self.send_push_notification_event_callback = None

    def set_send_push_notification_event_callback(self, callback):
        self.send_push_notification_event_callback = callback

    def send_push_notification(self, notification: str, cause="PHYSICAL_INTERACTION"):
        if self.send_push_notification_event_callback is not None :
            self.send_push_notification_event_callback(self.device_id, notification, cause)
