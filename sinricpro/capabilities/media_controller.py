class MediaController:
    def __init__(self, device_id):
        self.device_id = device_id
        self.on_media_control_callback = None

    def on_media_control(self, callback):
        self.on_media_control_callback = callback

    def set_send_media_control_event_callback(self, callback):
        self.send_media_control_event_callback = callback

    def send_media_control_event(self, media_control: str, cause="PHYSICAL_INTERACTION"):
        if self.send_media_control_event_callback is not None :
            self.send_media_control_event_callback(self.device_id, media_control, cause)
