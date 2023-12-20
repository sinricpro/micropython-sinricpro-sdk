from lib.capabilities.power_state_controller import PowerStateController

class SinricProSwitch(PowerStateController):
    def __init__(self, device_id):
        self.device_id = device_id

