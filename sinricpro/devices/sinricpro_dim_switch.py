from sinricpro.capabilities.power_level_controller import PowerLevelController
from sinricpro.capabilities.power_state_controller import PowerStateController
from sinricpro.capabilities.setting_controller import SettingController

class SinricProDimSwitch(PowerStateController, PowerLevelController, SettingController):
    """
    Represents a dim switch that can be controlled through SinricPro.
    """

    def __init__(self, device_id):
        """
        Initializes the SinricProDimSwitch object.

        Args:
            device_id (str): The unique identifier for the device in SinricPro.
        """

        super().__init__(device_id)
        self.device_id = device_id

