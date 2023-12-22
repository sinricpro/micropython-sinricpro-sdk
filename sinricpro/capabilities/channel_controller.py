class ChannelController:
    def __init__(self, device_id):
        self.device_id = device_id
        self.on_change_channel_callback = None
        self.on_change_channel_number_callback = None
        self.on_skip_channels_callback = None

    def on_change_channel(self, callback):
        self.on_change_channel_callback = callback

    def on_change_channel_number(self, callback):
        self.on_change_channel_number_callback = callback

    def on_skip_channels(self, callback):
        self.on_skip_channels_callback = callback

    def set_send_change_channel_event_callback(self, callback):
        self.send_change_channel_event_callback = callback

    def send_change_channel_event(self, channel_name: str, cause="PHYSICAL_INTERACTION"):
        if self.send_change_channel_event_callback is not None :
            self.send_change_channel_event_callback(self.device_id, channel_name, cause)
