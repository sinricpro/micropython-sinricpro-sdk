from sinricpro.capabilities.power_state_controller import PowerStateController
from sinricpro.capabilities.push_notification import PushNotificationController
from sinricpro.capabilities.setting_controller import SettingController
from sinricpro.capabilities.temperature_sensor import TemperatureSensor
from sinricpro.capabilities.thermostat_controller import ThermostatController

class SinricProThermostat(PowerStateController, SettingController, PushNotificationController, ThermostatController,
                       TemperatureSensor):
    """
    Device to control a TV
    """
    def __init__(self, device_id):
        super().__init__(device_id)
        self.device_id = device_id

