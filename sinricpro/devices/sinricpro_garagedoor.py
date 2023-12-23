from sinricpro.capabilities.mode_controller import ModeController
from sinricpro.capabilities.push_notification import PushNotificationController
from sinricpro.capabilities.setting_controller import SettingController

class SinricProGarageDoor(ModeController, SettingController, PushNotificationController):
    """
    Represents a garage door that can be controlled through SinricPro.
    """
    def __init__(self, device_id):
        """
        Initializes the SinricProGarageDoor object.

        Args:
            device_id (str): The unique identifier for the device in SinricPro.
        """

        super().__init__(device_id)
        self.device_id = device_id

