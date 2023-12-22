class PowerSensor:
    def __init__(self, device_id):
        self.device_id = device_id
        self.send_power_sensor_event_callback = None

    def set_send_power_sensor_event_callback(self, callback):
        self.send_power_sensor_event_callback = callback

    def send_power_sensor_event(self, start_time: int, voltage: float, current: float, power: float = -1.0, apparent_power: float = -1.0,
                                reactive_power: float = -1.0, factor: float = -1.0, cause="PHYSICAL_INTERACTION"):
        if self.send_power_sensor_event_callback is not None :
            self.send_power_sensor_event_callback(self.device_id, start_time, voltage, current, power, apparent_power,  reactive_power, factor,
                                                  cause)
