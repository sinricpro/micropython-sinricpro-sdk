from sinricpro.capabilities.lock_controller import LockController
from sinricpro.capabilities.push_notification import PushNotificationController
from sinricpro.capabilities.setting_controller import SettingController

class SinricProLock(LockController, SettingController, PushNotificationController):
    """
    Represents a smart lock that can be controlled through SinricPro.
    """
    def __init__(self, device_id):
        """
        Initializes the SinricProLock object.

        Args:
            device_id (str): The unique identifier for the device in SinricPro.
        """

        super().__init__(device_id)
        self.device_id = device_id

