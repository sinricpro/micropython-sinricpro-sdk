# Import the PowerStateController capability from the SinricPro library
from sinricpro.capabilities.power_state_controller import PowerStateController

class SinricProSwitch(PowerStateController):
    """
    Define a class for SinricProSwitch
    """
    def __init__(self, device_id):
        super().__init__()
        self.device_id = device_id

