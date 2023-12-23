from sinricpro.capabilities.range_controller import RangeController
from sinricpro.capabilities.power_state_controller import PowerStateController
from sinricpro.capabilities.push_notification import PushNotificationController
from sinricpro.capabilities.setting_controller import SettingController

class SinricProFan(PowerStateController, SettingController, PushNotificationController, RangeController):
    """
    Represents a fan that can be controlled through SinricPro.
    """
    def __init__(self, device_id):
        """
        Initializes the SinricProCamera object.

        Args:
            device_id (str): The unique identifier for the device in SinricPro.
        """
        super().__init__(device_id)
        self.device_id = device_id

