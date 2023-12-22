class ModeController:
    def __init__(self, device_id):
        self.device_id = device_id
        self.on_set_mode_callback = None
        self.on_set_mode_instance_callback = None
        self.send_mode_instance_event_callback = None
        self.on_set_mode_instances = {}

    def on_set_mode(self, callback):
        self.on_set_mode_callback = callback

    # def on_set_mode(self, instance: str, callback):
    #     self.on_set_mode_instances[instance] = callback

    def set_send_mode_event_callback(self, callback):
        self.send_mode_event_callback = callback

    # def set_send_mode_instance_event_callback(self, callback):
    #     self.send_mode_instance_event_callback = callback

    def send_mode_event(self, mode: str, cause="PHYSICAL_INTERACTION"):
        if self.send_mode_event_callback is not None :
            self.send_mode_event_callback(self.device_id, mode, cause)

    # def send_mode_event(self, instance: str, mode: str, cause="PHYSICAL_INTERACTION"):
    #     if self.send_mode_event_callback is not None :
    #         self.send_mode_event_callback(self.device_id, instance, mode, cause)
