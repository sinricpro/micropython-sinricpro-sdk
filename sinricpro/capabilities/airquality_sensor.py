class AirQualitySensor:
    def __init__(self, device_id):
        self.device_id = device_id

    def set_send_airquality_event_callback(self, callback):
        self.send_airquality_event_callback = callback

    def send_airquality_event(self, pm1: int, pm2_5: int, pm10: int, cause="PHYSICAL_INTERACTION"):
        if self.send_airquality_event_callback is not None :
            self.send_airquality_event_callback(self.device_id, pm1, pm2_5, pm10, cause)
