class SettingController:
    """
    Represents a device with adjustable settings within the SinricPro framework.
    """

    def __init__(self, device_id):
        """
        Initializes the SettingController object.

        Args:
            device_id (str): The unique identifier for the device in SinricPro.
        """

        self.device_id = device_id  # Store the device ID
        self.on_set_setting_callback = None  # Callback for handling setting changes

    def on_set_setting(self, callback):
        """
        Sets a callback function to be invoked when a setting is changed.

        Args:
            callback (function): A function that takes the following arguments:
                - setting (str): The name of the setting that was changed.
                - value (str): The new value of the setting.
        """

        self.on_set_setting_callback = callback
