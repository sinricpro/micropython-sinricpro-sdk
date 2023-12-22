class RangeController:
    def __init__(self, device_id):
        self.device_id = device_id
        self.on_range_value_callback = None
        self.on_adjust_range_value_callback = None
        self.n_range_value_instances = {}

    def on_range_value(self, callback):
        self.on_range_value_callback = callback

    def on_adjust_range_value(self, callback):
        self.on_adjust_range_value_callback = callback

    def set_send_range_value_event_callback(self, callback):
        self.send_range_value_event_callback = callback

    def send_range_value_event(self, range_value, cause="PHYSICAL_INTERACTION"):
        if self.send_range_value_event_callback is not None :
            self.send_range_value_event_callback(self.device_id, None, range_value, cause)

    def send_range_value_event(self, instance: str, range_value, cause="PHYSICAL_INTERACTION"):
        if self.send_range_value_event_callback is not None :
            self.send_range_value_event_callback(self.device_id, instance, range_value, cause)
