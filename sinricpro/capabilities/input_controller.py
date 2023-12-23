class InputController:
    """
    Represents an input controller device within the SinricPro framework.
    """

    def __init__(self, device_id):
        """
        Initializes the InputController object.

        Args:
            device_id (str): The unique identifier for the device in SinricPro.
        """

        self.device_id = device_id  # Store the device ID
        self.on_select_input_callback = None  # Callback for input selection
        self.send_select_input_event_callback = None  # Callback to send input select events

    def on_select_input(self, callback):
        """
        Sets a callback function to be invoked when an input is selected.

        Args:
            callback (function): A function that takes the following arguments:
                - input (str): The name of the selected input.
        """

        self.on_select_input_callback = callback

    def set_send_select_input_event_callback(self, callback):
        """ Internal use"""
        self.send_select_input_event_callback = callback

    def send_select_input_event(self, input: str, cause="PHYSICAL_INTERACTION"):
        """
        Sends an input select event notification to SinricPro.

        Args:
            input (str): The name of the selected input.
            cause (str, optional): The cause of the event (default: "PHYSICAL_INTERACTION").
        """

        if self.send_select_input_event_callback is not None:
            self.send_select_input_event_callback(self.device_id, input, cause)
