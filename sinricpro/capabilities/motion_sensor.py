class MotionSensor:
    def __init__(self, device_id):
        self.device_id = device_id
        self.send_motion_event_callback = None

    def set_send_motion_event_callback(self, callback):
        self.send_motion_event_callback = callback

    def send_motion_event(self, detected: bool, cause="PHYSICAL_INTERACTION"):
        if self.send_motion_event_callback is not None :
            self.send_motion_event_callback(self.device_id, detected, cause)
