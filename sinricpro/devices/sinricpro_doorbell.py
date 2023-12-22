# Import the PowerStateController capability from the SinricPro library
from sinricpro.capabilities.doorbell import Doorbell
from sinricpro.capabilities.push_notification import PushNotificationController
from sinricpro.capabilities.setting_controller import SettingController

class SinricProDoorbell(Doorbell, SettingController, PushNotificationController):
    """
    Device to report doorbell events
    """
    def __init__(self, device_id):
        super().__init__(device_id)
        self.device_id = device_id

