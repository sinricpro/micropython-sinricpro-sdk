class PowerLevelController:
    def __init__(self, device_id):
        self.device_id = device_id
        self.on_power_level_callback = None
        self.on_adjust_power_level_callback = None

    def on_power_level(self, callback):
        self.on_power_level_callback = callback

    def on_adjust_power_level(self, callback):
        self.on_adjust_power_level_callback = callback

    def set_send_power_level_event_callback(self, callback):
        self.send_power_level_event_callback = callback

    def send_power_level_event(self, power_level: int, cause="PHYSICAL_INTERACTION"):
        if self.send_power_level_event_callback is not None :
            self.send_power_level_event_callback(self.device_id, power_level, cause)
