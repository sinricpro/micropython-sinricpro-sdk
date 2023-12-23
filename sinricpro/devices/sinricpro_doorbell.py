# Import the PowerStateController capability from the SinricPro library
from sinricpro.capabilities.doorbell import Doorbell
from sinricpro.capabilities.push_notification import PushNotificationController
from sinricpro.capabilities.setting_controller import SettingController

class SinricProDoorbell(Doorbell, SettingController, PushNotificationController):
    """
    Represents a doorbell that can be controlled through SinricPro.
    """
    def __init__(self, device_id):
        """
        Initializes the SinricProDoorbell object.

        Args:
            device_id (str): The unique identifier for the device in SinricPro.
        """

        super().__init__(device_id)
        self.device_id = device_id

