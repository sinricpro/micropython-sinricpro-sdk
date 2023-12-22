from sinricpro.capabilities.power_level_controller import PowerLevelController
from sinricpro.capabilities.power_state_controller import PowerStateController
from sinricpro.capabilities.setting_controller import SettingController

class SinricProDimSwitch(PowerStateController, PowerLevelController, SettingController):
    """
    Device which supports on / off and dimming commands
    """
    def __init__(self, device_id):
        super().__init__(device_id)
        self.device_id = device_id

