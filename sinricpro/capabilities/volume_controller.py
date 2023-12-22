class VolumeController:
    def __init__(self, device_id):
        self.device_id = device_id
        self.on_set_volume_callback = None
        self.on_adjust_volume_callback = None

    def on_set_volume(self, callback):
        self.on_set_volume_callback = callback

    def on_adjust_volume(self, callback):
        self.on_adjust_volume_callback = callback

    def set_send_volume_event(self, callback):
        self.send_volume_event_callback = callback

    def send_volume_event(self, volume: int, cause="PHYSICAL_INTERACTION"):
        if self.send_volume_event_callback is not None:
            self.send_volume_event_callback(self.device_id, volume, cause)
