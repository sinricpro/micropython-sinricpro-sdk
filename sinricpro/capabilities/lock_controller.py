class LockController:
    """
    Represents a lock controller device within the SinricPro framework.
    """

    def __init__(self, device_id):
        """
        Initializes the LockController object.

        Args:
            device_id (str): The unique identifier for the device in SinricPro.
        """

        self.device_id = device_id  # Store the device ID
        self.on_lock_state_callback = None  # Callback for lock state updates
        self.send_lock_state_event_callback = None  # Callback to send lock state events

    def on_lock_state(self, callback):
        """
        Sets a callback function to be invoked when the lock state changes.

        Args:
            callback (function): A function that takes the following arguments:
                - state (bool): True if the lock is locked, False if unlocked.
        """

        self.on_lock_state_callback = callback

    def set_send_lock_state_event_callback(self, callback):
        """ Internal use"""
        self.send_lock_state_event_callback = callback

    def send_lock_state_event(self, state: bool, cause="PHYSICAL_INTERACTION"):
        """
        Sends a lock state event notification to SinricPro.

        Args:
            state (bool): The new lock state (True for locked, False for unlocked).
            cause (str, optional): The cause of the event (default: "PHYSICAL_INTERACTION").
        """

        if self.send_lock_state_event_callback is not None:
            self.send_lock_state_event_callback(self.device_id, state, cause)
