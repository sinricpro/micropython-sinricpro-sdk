class InputController:
    def __init__(self, device_id):
        self.device_id = device_id
        self.on_select_input_callback = None

    def on_select_input(self, callback):
        self.on_select_input_callback = callback

    def set_send_select_input_event_callback(self, callback):
        self.send_select_input_event_callback = callback

    def send_select_input_event(self, intput: str, cause="PHYSICAL_INTERACTION"):
        if self.send_select_input_event_callback is not None :
            self.send_select_input_event_callback(self.device_id, intput, cause)
