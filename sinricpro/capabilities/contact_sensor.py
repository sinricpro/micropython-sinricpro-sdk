class ContactSensor:
    def __init__(self, device_id):
        self.device_id = device_id

    def set_send_contact_event_callback(self, callback):
        self.send_contact_event_callback = callback

    def send_contact_event(self, detected: bool, cause="PHYSICAL_INTERACTION"):
        if self.send_contact_event_callback is not None :
            self.send_contact_event_callback(self.device_id, detected, cause)
