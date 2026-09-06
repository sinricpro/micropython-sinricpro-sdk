from sinricpro.capabilities.airquality_sensor import AirQualitySensor
from sinricpro.capabilities.push_notification import PushNotificationController
from sinricpro.capabilities.setting_controller import SettingController

class SinricProAirQualitySensor(AirQualitySensor, SettingController, PushNotificationController):
    """
    Represents an air quality sensor that can be controlled through SinricPro.
    """
    def __init__(self, device_id):
        """
        Initializes the SinricProAirQualitySensor object.

        Args:
            device_id (str): The unique identifier for the device in SinricPro.
        """
        super().__init__(device_id)
        self.device_id = device_id
