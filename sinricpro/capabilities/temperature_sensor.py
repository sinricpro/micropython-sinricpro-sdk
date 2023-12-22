class TemperatureSensor:
    def __init__(self, device_id):
        self.device_id = device_id
        self.send_temperature_event_callback = None

    def set_send_temperature_event_callback(self, callback):
        self.send_temperature_event_callback = callback

    def send_temperature_event(self, temperature: float, humidity: float = -1, cause="PERIODIC_POLL"):
        if self.send_temperature_event_callback is not None :
            self.send_temperature_event_callback(self.device_id, temperature, humidity, cause)
