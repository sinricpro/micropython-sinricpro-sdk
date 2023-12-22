from sinricpro.capabilities.power_state_controller import PowerStateController
from sinricpro.capabilities.push_notification import PushNotificationController
from sinricpro.capabilities.range_controller import RangeController
from sinricpro.capabilities.setting_controller import SettingController
from sinricpro.capabilities.thermostat_controller import ThermostatController

class SinricProWindowAC(PowerStateController, SettingController, PushNotificationController, RangeController, ThermostatController):
    """
    Device to control Window Air Conditioner
    """
    def __init__(self, device_id):
        super().__init__(device_id)
        self.device_id = device_id

