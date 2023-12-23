
from sinricpro.capabilities.contact_sensor import ContactSensor
from sinricpro.capabilities.push_notification import PushNotificationController
from sinricpro.capabilities.setting_controller import SettingController


class SinricProContactSensor(ContactSensor, PushNotificationController, SettingController):
    """
    Represents a contact sensor that can be controlled through SinricPro.
    """

    def __init__(self, device_id):
        """
        Initializes the SinricProContactSensor object.

        Args:
            device_id (str): The unique identifier for the device in SinricPro.
        """

        super().__init__(device_id)
        self.device_id = device_id

