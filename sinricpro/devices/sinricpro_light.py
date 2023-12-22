from sinricpro.capabilities.brightness_controller import BrightnessController
from sinricpro.capabilities.color_controller import ColorController
from sinricpro.capabilities.color_temperature_controller import ColorTemperatureController
from sinricpro.capabilities.power_state_controller import PowerStateController
from sinricpro.capabilities.setting_controller import SettingController

class SinricProLight(PowerStateController, BrightnessController, ColorController, SettingController, ColorTemperatureController):
    """
    Device to control a light
    """
    def __init__(self, device_id):
        super().__init__(device_id)
        self.device_id = device_id

