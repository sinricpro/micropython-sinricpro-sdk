from sinricpro.capabilities.power_state_controller import PowerStateController
from sinricpro.capabilities.push_notification import PushNotificationController
from sinricpro.capabilities.setting_controller import SettingController

class SinricProCamera(PushNotificationController, PowerStateController, SettingController):
    """
    Camera suporting basic on / off command
    """
    def __init__(self, device_id):
        super().__init__(device_id)
        self.device_id = device_id

