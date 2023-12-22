
from sinricpro.capabilities.power_state_controller import PowerStateController
from sinricpro.capabilities.push_notification import PushNotificationController
from sinricpro.capabilities.range_controller import RangeController
from sinricpro.capabilities.setting_controller import SettingController


class SinricProBlinds(PushNotificationController, PowerStateController, RangeController, SettingController):
    """
    Device to control interior blinds
    """
    def __init__(self, device_id):
        super().__init__(device_id)
        self.device_id = device_id

