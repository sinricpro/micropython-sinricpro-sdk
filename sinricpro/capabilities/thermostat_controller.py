class ThermostatController:
    def __init__(self, device_id):
        self.device_id = device_id
        self.on_thermostat_mode_callback = None
        self.on_target_temperature_callback = None
        self.on_adjust_target_temperature_callback = None

    def on_thermostat_mode(self, callback):
        self.on_thermostat_mode_callback = callback

    def on_target_temperature(self, callback):
        self.on_target_temperature_callback = callback

    def on_adjust_target_temperature(self, callback):
        self.on_adjust_target_temperature_callback = callback

    def set_send_thermostat_mode_event_callback(self, callback):
        self.send_thermostat_mode_event_callback = callback

    def send_thermostat_mode_event(self, thermostat_mode: str, cause="PHYSICAL_INTERACTION"):
        if self.send_thermostat_mode_event_callback is not None :
            self.send_thermostat_mode_event_callback(self.device_id, thermostat_mode, cause)

    def set_send_target_temperature_event_callback(self, callback):
        self.send_target_temperature_event_callback = callback

    def send_target_temperature_event(self, temperature: float, cause="PHYSICAL_INTERACTION"):
        if self.send_target_temperature_event_callback is not None :
            self.send_target_temperature_event_callback(self.device_id, temperature, cause)
