class PercentageController:
    def __init__(self, device_id):
        self.device_id = device_id
        self.on_set_percentage_callback = None
        self.on_adjust_percentage_callback = None

    def on_set_percentage(self, callback):
        self.on_set_percentage_callback = callback

    def on_adjust_percentage(self, callback):
        self.on_adjust_percentage_callback = callback

    def set_send_set_percentage_event_callback(self, callback):
        self.send_set_percentage_event_callback = callback

    def send_set_percentage_event(self, percentage: int, cause="PHYSICAL_INTERACTION"):
        if self.send_set_percentage_event_callback is not None :
            self.send_set_percentage_event_callback(self.device_id, percentage, cause)
