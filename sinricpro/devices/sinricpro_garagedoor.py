from sinricpro.capabilities.mode_controller import ModeController
from sinricpro.capabilities.push_notification import PushNotificationController
from sinricpro.capabilities.setting_controller import SettingController

class SinricProGarageDoor(ModeController, SettingController, PushNotificationController):
    """
    Device to control a garage door
    """
    def __init__(self, device_id):
        super().__init__(device_id)
        self.device_id = device_id

