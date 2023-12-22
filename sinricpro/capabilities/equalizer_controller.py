class EqualizerController:
    def __init__(self, device_id: str):
        self.device_id = device_id
        self.on_set_bands_callback = None
        self.on_adjust_bands_callback = None
        self.on_reset_bands_callback = None

    def on_set_bands(self, callback):
        self.on_set_bands_callback = callback

    def on_adjust_bands(self, callback):
        self.on_adjust_bands_callback = callback

    def on_reset_bands(self, callback):
        self.on_reset_bands_callback = callback

    def set_send_bands_event_callback(self, callback):
        self.send_bands_event_callback = callback

    def send_bands_event(self, bands: str, level: int, cause="PHYSICAL_INTERACTION"):
        if self.send_bands_event_callback is not None :
            self.send_bands_event_callback(self.device_id, bands, level, cause)
