class ToggleController:
    def __init__(self, device_id):
        self.device_id = device_id
        self.on_toggle_state_callback = None

    def on_toggle_state(self, callback):
        self.on_toggle_state_callback = callback

    def set_send_toggle_state_event_callback(self, callback):
        self.send_toggle_state_event_callback = callback

    def send_toggle_state_event(self, instance: str, state: bool, cause="PHYSICAL_INTERACTION"):
        if self.send_toggle_state_event_callback is not None:
            self.send_toggle_state_event_callback(self.device_id, instance, state, cause)
