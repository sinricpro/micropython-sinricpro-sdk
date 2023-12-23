from sinricpro.capabilities.push_notification import PushNotificationController
from sinricpro.capabilities.setting_controller import SettingController
from sinricpro.capabilities.temperature_sensor import TemperatureSensor

class SinricProTemperatureSensor(TemperatureSensor, SettingController, PushNotificationController):
    """
    Represents a temperature sensor that can be controlled through SinricPro.
    """
    def __init__(self, device_id):
        """
        Initializes the SinricProTemperatureSensor object.

        Args:
            device_id (str): The unique identifier for the device in SinricPro.
        """
        super().__init__(device_id)
        self.device_id = device_id

