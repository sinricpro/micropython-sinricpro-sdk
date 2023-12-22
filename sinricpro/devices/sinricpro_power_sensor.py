from sinricpro.capabilities.power_sensor import PowerSensor
from sinricpro.capabilities.push_notification import PushNotificationController
from sinricpro.capabilities.setting_controller import SettingController

class SinricProPowerSensor(PowerSensor, SettingController, PushNotificationController):
    """
    Device to report power usage
    """
    def __init__(self, device_id):
        super().__init__(device_id)
        self.device_id = device_id

