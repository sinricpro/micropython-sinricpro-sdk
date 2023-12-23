class ChannelController:
    """
    Represents a device that can control channels.
    """

    def __init__(self, device_id):
        """
        Initializes the ChannelController object.

        Args:
            device_id (str): The unique identifier for the device.
        """

        self.device_id = device_id  # Store the device ID
        self.on_change_channel_callback = None  # Callback for channel changes
        self.on_change_channel_number_callback = None  # Callback for channel number changes
        self.on_skip_channels_callback = None  # Callback for skipping channels
        self.send_change_channel_event_callback = None  # Callback to send channel change events

    def on_change_channel(self, callback):
        """
        Sets a callback function to be invoked when the channel is changed by name.

        Args:
            callback (function): A function that takes the following arguments:
                - channel_name (str): The name of the new channel.
        """

        self.on_change_channel_callback = callback

    def on_change_channel_number(self, callback):
        """
        Sets a callback function to be invoked when the channel is changed by number.

        Args:
            callback (function): A function that takes the following arguments:
                - channel_number (int): The number of the new channel.
        """

        self.on_change_channel_number_callback = callback

    def on_skip_channels(self, callback):
        """
        Sets a callback function to be invoked when a request to skip channels is received.

        Args:
            callback (function): A function that takes the following arguments:
                - number_of_channels_to_skip (int): The number of channels to skip.
        """

        self.on_skip_channels_callback = callback

    def set_send_change_channel_event_callback(self, callback):
        """ Internal use"""
        self.send_change_channel_event_callback = callback

    def send_change_channel_event(self, channel_name: str, cause="PHYSICAL_INTERACTION"):
        """
        Sends a channel change event notification.

        Args:
            channel_name (str): The name of the new channel.
            cause (str, optional): The cause of the event (default: "PHYSICAL_INTERACTION").
        """

        if self.send_change_channel_event_callback is not None:
            self.send_change_channel_event_callback(self.device_id, channel_name, cause)
