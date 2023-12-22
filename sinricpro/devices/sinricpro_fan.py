from sinricpro.capabilities.range_controller import RangeController
from sinricpro.capabilities.power_state_controller import PowerStateController
from sinricpro.capabilities.push_notification import PushNotificationController
from sinricpro.capabilities.setting_controller import SettingController

class SinricProFan(PowerStateController, SettingController, PushNotificationController, RangeController):
    """
    Device to turn on / off a fan and change it's speed
    """
    def __init__(self, device_id):
        super().__init__(device_id)
        self.device_id = device_id

