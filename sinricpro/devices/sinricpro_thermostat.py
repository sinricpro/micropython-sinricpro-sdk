from sinricpro.capabilities.power_state_controller import PowerStateController
from sinricpro.capabilities.push_notification import PushNotificationController
from sinricpro.capabilities.setting_controller import SettingController
from sinricpro.capabilities.temperature_sensor import TemperatureSensor
from sinricpro.capabilities.thermostat_controller import ThermostatController

class SinricProThermostat(PowerStateController, SettingController, PushNotificationController, ThermostatController,
                       TemperatureSensor):
    """
    Represents a thermostat that can be controlled through SinricPro.
    """
    def __init__(self, device_id):
        """
        Initializes the SinricProThermostat object.

        Args:
            device_id (str): The unique identifier for the device in SinricPro.
        """

        super().__init__(device_id)
        self.device_id = device_id

