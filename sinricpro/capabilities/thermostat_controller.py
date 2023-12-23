class ThermostatController:
    """
    Represents a thermostat device within the SinricPro framework.
    """

    def __init__(self, device_id):
        """
        Initializes the ThermostatController object.

        Args:
            device_id (str): The unique identifier for the device in SinricPro.
        """

        self.device_id = device_id  # Store the device ID
        self.on_thermostat_mode_callback = None  # Callback for thermostat mode changes
        self.on_target_temperature_callback = None  # Callback for target temperature changes
        self.on_adjust_target_temperature_callback = None  # Callback for adjusting target temperature

    def on_thermostat_mode(self, callback):
        """
        Sets a callback function to be invoked when the thermostat mode changes.

        Args:
            callback (function): A function that takes the following argument:
                - thermostat_mode (str): The new thermostat mode (e.g., "HEAT", "COOL", "AUTO").
        """

        self.on_thermostat_mode_callback = callback

    def on_target_temperature(self, callback):
        """
        Sets a callback function to be invoked when the target temperature changes.

        Args:
            callback (function): A function that takes the following argument:
                - temperature (float): The new target temperature.
        """

        self.on_target_temperature_callback = callback

    def on_adjust_target_temperature(self, callback):
        """
        Sets a callback function to be invoked when the target temperature is adjusted by a relative amount.

        Args:
            callback (function): A function that takes the following argument:
                - delta (float): The amount to adjust the target temperature by (positive or negative).
        """

        self.on_adjust_target_temperature_callback = callback

    def set_send_thermostat_mode_event_callback(self, callback):
        """ Internal use"""
        self.send_thermostat_mode_event_callback = callback

    def send_thermostat_mode_event(self, thermostat_mode: str, cause="PHYSICAL_INTERACTION"):
        """
        Sends a thermostat mode event notification to SinricPro.

        Args:
            thermostat_mode (str): The new thermostat mode.
            cause (str, optional): The cause of the event (default: "PHYSICAL_INTERACTION").
        """

        if self.send_thermostat_mode_event_callback is not None:
            self.send_thermostat_mode_event_callback(self.device_id, thermostat_mode, cause)

    def set_send_target_temperature_event_callback(self, callback):
        """ Internal use"""
        self.send_target_temperature_event_callback = callback

    def send_target_temperature_event(self, temperature: float, cause="PHYSICAL_INTERACTION"):
        """
        Sends a target temperature event notification to SinricPro.

        Args:
            temperature (float): The new target temperature.
            cause (str, optional): The cause of the event (default: "PHYSICAL_INTERACTION").
        """

        if self.send_target_temperature_event_callback is not None:
            self.send_target_temperature_event_callback(self.device_id, temperature, cause)
