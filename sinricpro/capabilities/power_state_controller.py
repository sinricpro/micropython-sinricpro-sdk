class PowerStateController:
    def __init__(self, device_id):
        self.device_id = device_id
        self.power_state_callback = None
        self.send_power_state_event_callback = None

    def on_power_state(self, callback):
        self.power_state_callback = callback

    def set_send_power_state_event_callback(self, callback):
        self.send_power_state_event_callback = callback

    def send_power_state_event(self, state: bool, cause="PHYSICAL_INTERACTION"):
        self.send_power_state_event_callback(self.device_id, state, cause)
