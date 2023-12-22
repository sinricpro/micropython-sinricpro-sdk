from sinricpro.capabilities.motion_sensor import MotionSensor
from sinricpro.capabilities.push_notification import PushNotificationController
from sinricpro.capabilities.setting_controller import SettingController

class SinricProMotionSensor(MotionSensor, SettingController, PushNotificationController):
    """
    Device to report motion detection events
    """
    def __init__(self, device_id):
        super().__init__(device_id)
        self.device_id = device_id

