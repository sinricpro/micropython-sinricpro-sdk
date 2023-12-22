from sinricpro.capabilities.equalizer_controller import EqualizerController
from sinricpro.capabilities.input_controller import InputController
from sinricpro.capabilities.media_controller import MediaController
from sinricpro.capabilities.mode_controller import ModeController
from sinricpro.capabilities.mute_controller import MuteController
from sinricpro.capabilities.power_state_controller import PowerStateController
from sinricpro.capabilities.push_notification import PushNotificationController
from sinricpro.capabilities.setting_controller import SettingController
from sinricpro.capabilities.volume_controller import VolumeController

class SinricProSpeaker(PowerStateController, SettingController, PushNotificationController, MuteController,
                       VolumeController, MediaController, InputController, EqualizerController, ModeController):
    """
    Device to control a smart speaker
    """
    def __init__(self, device_id):
        super().__init__(device_id)
        self.device_id = device_id

