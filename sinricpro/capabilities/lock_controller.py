class LockController:
    def __init__(self, device_id):
        self.device_id = device_id
        self.on_lock_state_callback = None

    def on_lock_state(self, callback):
        self.on_lock_state_callback = callback

    def set_send_lock_state_event_callback(self, callback):
        self.send_lock_state_event_callback = callback

    def send_lock_state_event(self, state: bool, cause="PHYSICAL_INTERACTION"):
        if self.send_lock_state_event_callback is not None :
            self.send_lock_state_event_callback(self.device_id, state, cause)
