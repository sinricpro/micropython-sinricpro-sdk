from sinricpro.capabilities.power_sensor import PowerSensor
from sinricpro.capabilities.push_notification import PushNotificationController
from sinricpro.capabilities.setting_controller import SettingController

class SinricProPowerSensor(PowerSensor, SettingController, PushNotificationController):
    """
    Represents a power sensor or power meter that can be controlled through SinricPro.
    """
    def __init__(self, device_id):
        """
        Initializes the SinricProPowerSensor object.

        Args:
            device_id (str): The unique identifier for the device in SinricPro.
        """
        super().__init__(device_id)
        self.device_id = device_id

