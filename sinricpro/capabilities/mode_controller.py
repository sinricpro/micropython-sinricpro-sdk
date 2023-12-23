class ModeController:
    """
    Represents a device with different operating modes within the SinricPro framework.
    """

    def __init__(self, device_id):
        """
        Initializes the ModeController object.

        Args:
            device_id (str): The unique identifier for the device in SinricPro.
        """

        self.device_id = device_id  # Store the device ID
        self.on_set_mode_callback = None  # Callback for general mode changes
        self.on_set_mode_instance_callback = None  # Callback for mode changes for specific instances
        self.send_mode_instance_event_callback = None  # Callback for sending mode instance events
        self.on_set_mode_instances = {}  # Dictionary to store callbacks for specific mode instances

    def on_set_mode(self, callback):
        """
        Sets a callback function to be invoked when the overall mode of the device changes.

        Args:
            callback (function): A function that takes the following argument:
                - mode (str): The new mode of the device.
        """

        self.on_set_mode_callback = callback

    def set_send_mode_event_callback(self, callback):
        """ Internal use"""
        self.send_mode_event_callback = callback

    def send_mode_event(self, mode: str, cause="PHYSICAL_INTERACTION"):
        """
        Sends a mode event notification to SinricPro.

        Args:
            mode (str): The new mode.
            cause (str, optional): The cause of the event (default: "PHYSICAL_INTERACTION").
        """

        if self.send_mode_event_callback is not None:
            self.send_mode_event_callback(self.device_id, mode, cause)


    # def on_set_mode(self, instance: str, callback):
    #     self.on_set_mode_instances[instance] = callback

    # def set_send_mode_instance_event_callback(self, callback):
    #     self.send_mode_instance_event_callback = callback

    # def send_mode_event(self, instance: str, mode: str, cause="PHYSICAL_INTERACTION"):
    #     if self.send_mode_event_callback is not None :
    #         self.send_mode_event_callback(self.device_id, instance, mode, cause)
