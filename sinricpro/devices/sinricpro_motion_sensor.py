from sinricpro.capabilities.motion_sensor import MotionSensor
from sinricpro.capabilities.push_notification import PushNotificationController
from sinricpro.capabilities.setting_controller import SettingController

class SinricProMotionSensor(MotionSensor, SettingController, PushNotificationController):
    """
    Represents a motion sensor that can be controlled through SinricPro.
    """
    def __init__(self, device_id):
        """
        Initializes the SinricProMotionSensor object.

        Args:
            device_id (str): The unique identifier for the device in SinricPro.
        """
        super().__init__(device_id)
        self.device_id = device_id

