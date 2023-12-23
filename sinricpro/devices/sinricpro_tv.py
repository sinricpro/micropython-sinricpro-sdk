from sinricpro.capabilities.channel_controller import ChannelController
from sinricpro.capabilities.equalizer_controller import EqualizerController
from sinricpro.capabilities.input_controller import InputController
from sinricpro.capabilities.media_controller import MediaController
from sinricpro.capabilities.mode_controller import ModeController
from sinricpro.capabilities.mute_controller import MuteController
from sinricpro.capabilities.power_state_controller import PowerStateController
from sinricpro.capabilities.push_notification import PushNotificationController
from sinricpro.capabilities.setting_controller import SettingController
from sinricpro.capabilities.volume_controller import VolumeController

class SinricProTV(PowerStateController, SettingController, PushNotificationController, MuteController,
                       VolumeController, MediaController, InputController, EqualizerController, ModeController,
                       ChannelController):
    """
    Represents a smart tv that can be controlled through SinricPro.
    """
    def __init__(self, device_id):
        """
        Initializes the SinricProTV object.

        Args:
            device_id (str): The unique identifier for the device in SinricPro.
        """

        super().__init__(device_id)
        self.device_id = device_id

