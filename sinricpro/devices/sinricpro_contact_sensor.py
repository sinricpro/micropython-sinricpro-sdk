
from sinricpro.capabilities.contact_sensor import ContactSensor
from sinricpro.capabilities.push_notification import PushNotificationController
from sinricpro.capabilities.setting_controller import SettingController


class SinricProContactSensor(ContactSensor, PushNotificationController, SettingController):
    """
    Device to report contact sensor events
    """
    def __init__(self, device_id):
        super().__init__(device_id)
        self.device_id = device_id

