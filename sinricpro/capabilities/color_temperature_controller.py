class ColorTemperatureController:
    def __init__(self, device_id):
        self.device_id = device_id
        self.on_color_temperature_callback = None
        self.on_increase_color_temperature_callback = None
        self.on_decrease_color_temperature = None

    def on_color_temperature(self, callback):
        self.on_color_temperature_callback = callback

    def on_increase_color_temperature(self, callback):
        self.on_increase_color_temperature_callback = callback

    def on_decrease_color_temperature(self, callback):
        self.on_decrease_color_temperature_callback = callback

    def set_send_color_temperature_event_callback(self, callback):
        self.send_color_temperature_event_callback = callback

    def send_color_temperature_event(self, color_temperature: int, cause="PHYSICAL_INTERACTION"):
        if self.send_color_temperature_event_callback is not None :
            self.send_color_temperature_event_callback(self.device_id, color_temperature, cause)
