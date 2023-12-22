# Import the PowerStateController capability from the SinricPro library
from sinricpro.capabilities.power_state_controller import PowerStateController
from sinricpro.capabilities.push_notification import PushNotificationController
from sinricpro.capabilities.setting_controller import SettingController

class SinricProSwitch(PowerStateController, SettingController, PushNotificationController):
    """
    Device suporting basic on / off command
    """
    def __init__(self, device_id):
        super().__init__(device_id)
        self.device_id = device_id

