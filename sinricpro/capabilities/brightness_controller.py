class BrightnessController:
    def __init__(self, device_id):
        self.device_id = device_id
        self.on_brightness_callback = None
        self.on_adjust_brightness_callback = None

    def on_brightness(self, callback):
        self.on_brightness_callback = callback

    def on_adjust_brightness(self, callback):
        self.on_adjust_brightness_callback = callback

    def set_send_brightness_event_callback(self, callback):
        self.send_brightness_event_callback = callback

    def send_brightness_event(self, brightness: int, cause="PHYSICAL_INTERACTION"):
        if self.send_brightness_event_callback is not None:
            self.send_brightness_event_callback(self.device_id, brightness, cause)
