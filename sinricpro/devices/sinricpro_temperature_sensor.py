from sinricpro.capabilities.push_notification import PushNotificationController
from sinricpro.capabilities.setting_controller import SettingController
from sinricpro.capabilities.temperature_sensor import TemperatureSensor

class SinricProTemperatureSensor(TemperatureSensor, SettingController, PushNotificationController):
    """
    Device to report actual temperature and humidity
    """
    def __init__(self, device_id):
        super().__init__(device_id)
        self.device_id = device_id

