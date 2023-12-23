class PowerSensor:
    """
    Represents a power sensor device within the SinricPro framework.
    """

    def __init__(self, device_id):
        """
        Initializes the PowerSensor object.

        Args:
            device_id (str): The unique identifier for the device in SinricPro.
        """

        self.device_id = device_id  # Store the device ID
        self.send_power_sensor_event_callback = None  # Callback for sending power sensor events

    def set_send_power_sensor_event_callback(self, callback):
        """ Internal use"""
        self.send_power_sensor_event_callback = callback

    def send_power_sensor_event(self, start_time: int, voltage: float, current: float, power: float = -1.0, apparent_power: float = -1.0,
                                 reactive_power: float = -1.0, factor: float = -1.0, cause="PHYSICAL_INTERACTION"):
        """
        Sends a power sensor event notification to SinricPro.

        Args:
            start_time (int): The timestamp (in milliseconds) when the measurement was taken.
            voltage (float): The measured voltage.
            current (float): The measured current.
            power (float, optional): The measured power (default: -1.0 if not available).
            apparent_power (float, optional): The measured apparent power (default: -1.0 if not available).
            reactive_power (float, optional): The measured reactive power (default: -1.0 if not available).
            factor (float, optional): The power factor (default: -1.0 if not available).
            cause (str, optional): The cause of the event (default: "PHYSICAL_INTERACTION").
        """

        if self.send_power_sensor_event_callback is not None:
            self.send_power_sensor_event_callback(self.device_id, start_time, voltage, current, power, apparent_power, reactive_power, factor, cause)
