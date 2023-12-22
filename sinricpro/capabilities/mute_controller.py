class MuteController:
    def __init__(self, device_id):
        self.device_id = device_id
        self.on_mute_callback = None

    def on_mute(self, callback):
        self.on_mute_callback = callback

    def set_send_mute_event_callback(self, callback):
        self.send_mute_event_callback = callback

    def send_mute_event(self, mute: bool, cause="PHYSICAL_INTERACTION"):
        if self.send_mute_event_callback is not None :
            self.send_mute_event_callback(self.device_id, mute, cause)
