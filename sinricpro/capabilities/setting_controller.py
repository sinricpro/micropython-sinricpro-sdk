class SettingController:
    def __init__(self, device_id):
        self.device_id = device_id
        self.on_set_setting_callback = None

    def on_set_setting(self, callback):
        self.on_set_setting_callback = callback
