from sinricpro.capabilities.lock_controller import LockController
from sinricpro.capabilities.push_notification import PushNotificationController
from sinricpro.capabilities.setting_controller import SettingController

class SinricProLock(LockController, SettingController, PushNotificationController):
    """
    Device to control a smart lock
    """
    def __init__(self, device_id):
        super().__init__(device_id)
        self.device_id = device_id

