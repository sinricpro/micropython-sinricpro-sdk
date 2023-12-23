from sinricpro.capabilities.brightness_controller import BrightnessController
from sinricpro.capabilities.color_controller import ColorController
from sinricpro.capabilities.color_temperature_controller import ColorTemperatureController
from sinricpro.capabilities.power_state_controller import PowerStateController
from sinricpro.capabilities.setting_controller import SettingController

class SinricProLight(PowerStateController, BrightnessController, ColorController, SettingController, ColorTemperatureController):
    """
    Represents a smart light bulb that can be controlled through SinricPro.
    """
    def __init__(self, device_id):
        """
        Initializes the SinricProLight object.

        Args:
            device_id (str): The unique identifier for the device in SinricPro.
        """

        super().__init__(device_id)
        self.device_id = device_id

