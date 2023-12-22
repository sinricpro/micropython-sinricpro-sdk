class ColorController:
    def __init__(self, device_id):
        self.device_id = device_id
        self.on_color_callback = None

    def on_color(self, callback):
        self.on_color_callback = callback

    def set_send_color_event_callback(self, callback):
        self.send_color_event_callback = callback

    def send_color_event(self, r: int, g: int, b: int, cause="PHYSICAL_INTERACTION"):
        if self.send_color_event_callback is not None :
            self.send_color_event_callback(self.device_id, r, g, b, cause)
