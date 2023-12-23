import uasyncio
import json
import gc
import time
from sinricpro.async_websocket_client import AsyncWebsocketClient
from sinricpro.async_queue import AsyncQueue
from sinricpro.exceptions import exceptions
from sinricpro.sinricpro_constants import SinricProConstants
from sinricpro.utils.utilities import is_null_or_empty
from sinricpro.utils.signer import Signer
from sinricpro.utils.logging import getLogger, DEBUG, ERROR
from sinricpro.capabilities.power_state_controller import PowerStateController
from sinricpro.utils.rate_limiter import RateLimiter
from sinricpro.utils.timestamp import Timestamp
from sinricpro.capabilities.brightness_controller import BrightnessController
from sinricpro.capabilities.channel_controller import ChannelController
from sinricpro.capabilities.color_controller import ColorController
from sinricpro.capabilities.color_temperature_controller import ColorTemperatureController
from sinricpro.capabilities.contact_sensor import ContactSensor
from sinricpro.capabilities.door_controller import DoorController
from sinricpro.capabilities.doorbell import Doorbell
from sinricpro.capabilities.equalizer_controller import EqualizerController
from sinricpro.capabilities.input_controller import InputController
from sinricpro.capabilities.lock_controller import LockController
from sinricpro.capabilities.media_controller import MediaController
from sinricpro.capabilities.mode_controller import ModeController
from sinricpro.capabilities.motion_sensor import MotionSensor
from sinricpro.capabilities.mute_controller import MuteController
from sinricpro.capabilities.percentage_controller import PercentageController
from sinricpro.capabilities.power_level_controller import PowerLevelController
from sinricpro.capabilities.power_sensor import PowerSensor
from sinricpro.capabilities.push_notification import PushNotificationController
from sinricpro.capabilities.range_controller import RangeController
from sinricpro.capabilities.temperature_sensor import TemperatureSensor
from sinricpro.capabilities.thermostat_controller import ThermostatController
from sinricpro.capabilities.toggle_controller import ToggleController
from sinricpro.capabilities.volume_controller import VolumeController

class SinricPro:
    "The SinricPro class handles device registration, event handling, and communication with the Sinric Pro server."

    def __init__(self):
        self.devices = []
        self.ws = AsyncWebsocketClient() # create instance of websocket
        self.publish_queue = AsyncQueue(5) # create publish queue
        self.received_queue = AsyncQueue(5) # create publish queue
        self.signer = Signer()
        self.sdkversion = '0.0.1' # todo: read from settings?
        self.log = getLogger("SinricPro")
        self.limiter = RateLimiter(60)
        self.timestamp = Timestamp()

    def add_device(self, device) -> None:
        """
        Add a device to internal device collection.
        """
        self.devices.append(device)

    async def _connect(self) -> None:
        """
        Establishes the websocket connection to the Sinric Pro server.
        """

        # Prepare device IDs for the connection:
        device_ids = []
        for device in self.devices:
            device_ids.append(device.device_id)
            if self.enable_log :
                self.log.debug(f"Adding {device.device_id}.")

        # Create WebSocket headers for the connection:
        headers = []
        headers.append(("appkey", self.app_key))
        headers.append(("deviceids", ';'.join(device_ids)))
        headers.append(("platform", 'micropython'))
        headers.append(('restoredevicestates', ('true' if self.restore_device_states else 'false')))
        headers.append(("sdkversion", self.sdkversion))

        if self.enable_log :
            self.log.debug(f"Connecting to {self.server_url}")

        # Initiate the WebSocket handshake:
        if not await self.ws.handshake(self.server_url, headers=headers):
            self.log.error("Connection failed!")
            raise RuntimeError("Cannot connect to SinricPro server!.")

        if self.enable_log :
            self.log.debug("Connected!")

        while await self.ws.open():
            data = await self.ws.recv()
            if self.enable_log :
                self.log.debug('<-{}'.format(str(data)))

            if data:
                self.received_queue.put(str(data)) # Put data in a queue for further handling
            gc.collect()

    def _get_response_json(self, message_dict, success, value_dict, instance_id='') -> str:
        """
        Returns the response for a request.
        """
        header = {
            "payloadVersion": 2,
            "signatureVersion": 1
        }

        payload = {
            "action": message_dict['payload']['action'],
            "clientId": message_dict['payload']['clientId'],
            "createdAt": message_dict['payload']['createdAt'],
            "deviceId": message_dict['payload']['deviceId'],
            "message": "OK",
            "replyToken": message_dict['payload']['replyToken'],
            "success": success,
            "type": "response",
            "value": value_dict
        }

        if instance_id:
            payload['instanceId'] = instance_id

        signature = self.signer.get_signature(self.app_secret, payload)
        return json.dumps({"header": header, "payload": payload, "signature": signature})

    def _get_event_json(self, action:str, device_id:str, value:str, type_of_interaction:str="PHYSICAL_INTERACTION", instance_id=None) -> str:
        """
        Returns event json.
        """
        epoch = self.timestamp.get_timestamp()

        header = {
            "payloadVersion": 2,
            "signatureVersion": 1
        }

        payload = {
            "action": action,
            "cause": {
                "type": type_of_interaction
            },
            "createdAt": epoch,
            "deviceId": device_id,
            "type": "event",
            "value": value
        }

        if instance_id:
            payload['instanceId'] = instance_id

        signature = self.signer.get_signature(self.app_secret, payload)
        return json.dumps( {"header": header, "payload": payload, "signature": signature} )


    async def _handle_received_request(self, message_dict, action) -> None:
        """
        Processes incoming requests from the server, invoking device-specific callbacks for actions like turning on/off, adjusting brightness, etc.
        """

        try:
            target_device_id = message_dict['payload']['deviceId']

            # look for the device id and invoke the callback
            for device in self.devices:
                if device.device_id == target_device_id :
                    success = False
                    instance_id=None

                    if action == SinricProConstants.SET_POWER_STATE:
                        state = message_dict['payload']['value']['state'] == "On"
                        if device.power_state_callback is not None:
                            success = await device.power_state_callback(target_device_id, state)
                        else:
                            self.log.error("callback 'power_state' isn't defined")

                    elif action == SinricProConstants.SET_POWER_LEVEL:
                        power_level = message_dict['payload']['value']['powerLevel']
                        if device.on_power_level_callback is not None:
                            success = await device.on_power_level_callback(target_device_id, power_level)
                        else:
                            self.log.error("callback 'on_power_level' isn't defined")

                    elif action == SinricProConstants.ADJUST_POWER_LEVEL:
                        power_level_delta = message_dict['payload']['value']['powerLevelDelta']
                        if device.on_adjust_power_level_callback is not None:
                            success = await device.on_adjust_power_level_callback(target_device_id, power_level_delta)
                        else:
                            self.log.error("callback 'on_adjust_power_level' isn't defined")

                    elif action == SinricProConstants.SET_BRIGHTNESS:
                        brightness = message_dict['payload']['value']['brightness']
                        if device.on_brightness_callback is not None:
                            success = await device.on_brightness_callback(target_device_id, brightness)
                        else:
                            self.log.error("callback 'on_brightness' isn't defined")

                    elif action == SinricProConstants.ADJUST_BRIGHTNESS:
                        brightness_delta = message_dict['payload']['value']['brightnessDelta']
                        if device.on_adjust_brightness_callback is not None:
                            success = await device.on_adjust_brightness_callback(target_device_id, brightness_delta)
                        else:
                            self.log.error("callback 'on_adjust_brightness' isn't defined")

                    elif action == SinricProConstants.SET_COLOR:
                        color = message_dict['payload']['value']['color']
                        if device.on_color_callback is not None:
                            success = await device.on_color_callback(target_device_id, color["r"], color["g"], color["b"])
                        else:
                            self.log.error("callback 'on_color' isn't defined")

                    elif action == SinricProConstants.SET_COLOR_TEMPERATURE:
                        color_temperature = message_dict['payload']['value']['colorTemperature']
                        if device.on_color_temperature_callback is not None:
                            success = await device.on_color_temperature_callback(target_device_id, color_temperature)
                        else:
                            self.log.error("callback 'on_color_temperature' isn't defined")

                    elif action == SinricProConstants.INCREASE_COLOR_TEMPERATURE:
                        if device.on_increase_color_temperature_callback is not None:
                            success = await device.on_increase_color_temperature_callback(target_device_id)
                        else:
                            self.log.error("callback 'on_increase_color_temperature' isn't defined")

                    elif action == SinricProConstants.DECREASE_COLOR_TEMPERATURE:
                        if device.on_decrease_color_temperature_callback is not None:
                            success = await device.on_decrease_color_temperature_callback(target_device_id)
                        else:
                            self.log.error("callback 'on_decrease_color_temperature' isn't defined")

                    elif action == SinricProConstants.SET_THERMOSTAT_MODE:
                        thermostat_mode = message_dict['payload']['value']['thermostatMode']
                        if device.on_thermostat_mode_callback is not None:
                            success = await device.on_thermostat_mode_callback(target_device_id, thermostat_mode)
                        else:
                            self.log.error("callback 'on_thermostat_mode' isn't defined")

                    elif action == SinricProConstants.SET_RANGE_VALUE:
                        range_value = message_dict['payload']['value']['rangeValue']

                        if "instanceId" in message_dict:
                            instance_id = message_dict['instanceId']
                            if device.on_range_value_callback is not None:
                                success = await self.on_range_value_instances[instance_id](target_device_id, range_value)
                        else:
                            if device.on_range_value_callback is not None:
                                success = await device.on_range_value_callback(target_device_id, range_value)
                            else:
                                self.log.error("callback 'on_range_value' isn't defined")

                    elif action == SinricProConstants.ADJUST_RANGE_VALUE:
                        range_value_delta = message_dict['payload']['value']['rangeValueDelta']
                        if device.on_adjust_range_value_callback is not None:
                            success = await device.on_adjust_range_value_callback(target_device_id, range_value_delta)
                        else:
                            self.log.error("callback 'on_adjust_range_value' isn't defined")

                    elif action == SinricProConstants.TARGET_TEMPERATURE:
                        temperature = message_dict['payload']['value']['temperature']
                        if device.on_target_temperature_callback is not None:
                            success = await device.on_target_temperature_callback(target_device_id, temperature)
                        else:
                            self.log.error("callback 'on_target_temperature' isn't defined")

                    elif action == SinricProConstants.ADJUST_TARGET_TEMPERATURE:
                        temperature = message_dict['payload']['value']['temperature']
                        if device.on_adjust_target_temperature_callback is not None:
                            success = await device.on_adjust_target_temperature_callback(target_device_id, temperature)
                        else:
                            self.log.error("callback 'on_adjust_target_temperature' isn't defined")

                    elif action == SinricProConstants.SET_VOLUME:
                        volume = message_dict['payload']['value']['volume']
                        if device.on_set_volume_callback is not None:
                            success = await device.on_set_volume_callback(target_device_id, volume)
                        else:
                            self.log.error("callback 'on_set_volume' isn't defined")

                    elif action == SinricProConstants.ADJUST_VOLUME:
                        volume = message_dict['payload']['value']['volume']
                        if device.on_adjust_volume_callback is not None:
                            success = await device.on_adjust_volume_callback(target_device_id, volume)
                        else:
                            self.log.error("callback 'on_adjust_volume' isn't defined")

                    elif action == SinricProConstants.MEDIA_CONTROL:
                        control = message_dict['payload']['value']['control']
                        if device.on_media_control_callback is not None:
                            success = await device.on_media_control_callback(target_device_id, control)
                        else:
                            self.log.error("callback 'on_media_control' isn't defined")

                    elif action == SinricProConstants.SELECT_INPUT:
                        selected_input = message_dict['payload']['value']['input']
                        if device.on_select_input_callback is not None:
                            success = await device.on_select_input_callback(target_device_id, selected_input)
                        else:
                            self.log.error("callback 'on_select_input' isn't defined")

                    elif action == SinricProConstants.SKIP_CHANNELS:
                        channel_count = message_dict['payload']['value']['channelCount']
                        if device.on_skip_channels_callback is not None:
                            success = await device.on_skip_channels_callback(target_device_id, channel_count)
                        else:
                            self.log.error("callback 'on_skip_channels' isn't defined")

                    elif action == SinricProConstants.SET_MUTE:
                        mute = message_dict['payload']['value']['mute']
                        if device.on_mute_callback is not None:
                            success = await device.on_mute_callback(target_device_id, mute)
                        else:
                            self.log.error("callback 'on_mute' isn't defined")

                    elif action == SinricProConstants.SET_BANDS:
                        bands = message_dict['payload']['value']['bands']
                        if device.on_set_bands_callback is not None:
                            success = await device.on_set_bands_callback(target_device_id, bands)
                        else:
                            self.log.error("callback 'on_set_bands' isn't defined")

                    elif action == SinricProConstants.ADJUST_BANDS:
                        bands = message_dict['payload']['value']['bands']
                        if device.on_adjust_bands_callback is not None:
                            success = await device.on_adjust_bands_callback(target_device_id, bands)
                        else:
                            self.log.error("callback 'on_adjust_bands' isn't defined")

                    elif action == SinricProConstants.RESET_BANDS:
                        bands = message_dict['payload']['value']['bands']
                        if device.on_reset_bands_callback is not None:
                            success = await device.on_reset_bands_callback(target_device_id, bands)
                        else:
                            self.log.error("callback 'on_reset_bands' isn't defined")

                    elif action == SinricProConstants.SET_MODE:
                        mode = message_dict['payload']['value']['mode']
                        if "instanceId" in message_dict:
                            instance_id = message_dict['instanceId']
                            if device.on_set_mode_callback is not None:
                                success = await self.on_set_mode_instances[instance_id](target_device_id, mode)
                            else:
                                self.log.error("callback 'on_set_mode' isn't defined")
                        else:
                            if device.on_set_mode_callback is not None:
                                success = await device.on_set_mode_callback(target_device_id, mode)
                            else:
                                self.log.error("callback 'on_set_mode' isn't defined")

                    elif action == SinricProConstants.SET_LOCK_STATE:
                        state = message_dict['payload']['value']['state']
                        if device.on_lock_state_callback is not None:
                            success = await device.on_lock_state_callback(target_device_id, state)
                            if success:
                                message_dict['payload']['value']["state"] = f"{state.upper()}ED"
                        else:
                            self.log.error("callback 'on_lock_state' isn't defined")

                    elif action == SinricProConstants.SET_PRECENTAGE:
                        percentage = message_dict['payload']['value']['state']
                        if device.on_set_percentage_callback is not None:
                            success = await device.on_set_percentage_callback(target_device_id, percentage)
                        else:
                            self.log.error("callback 'on_set_percentage' isn't defined")

                    elif action == SinricProConstants.SET_TOGGLE_STATE:
                        state = message_dict['payload']['value']['state']
                        if device.on_toggle_state_callback is not None:
                            success = await device.on_toggle_state_callback(target_device_id, percentage)
                        else:
                            self.log.error("callback 'on_toggle_state' isn't defined")

                    value_dict = message_dict['payload']['value']
                    response = self._get_response_json(message_dict=message_dict, success=success, value_dict=value_dict, instance_id=instance_id)
                    self.publish_queue.put(response)
                    break

        except Exception as e:
            self.log.error(f'Error : {e}')


    async def _process_publish_queue(self) -> None:
        """
        Sends outgoing messages (events or responses) to the server.
        """
        try:
            async for message in self.publish_queue:
                if self.enable_log :
                    self.log.info('-> : {}'.format(message))
                await self.ws.send(message)
        except Exception as e:
            self.log.error(f'Error : {e}')

    async def _process_received_queue(self) -> None:
        """
        Processes incoming messages from the server.
        """
        async for message in self.received_queue:
            message_dict = json.loads(message)

            if "timestamp" in message_dict:
                if self.enable_log :
                    self.log.debug("Got TimeStamp!")
                    # sending events needs timestamp.
                    self.timestamp.set_timestamp(message_dict["timestamp"])
            else:
                # verify signature
                if not self.signer.verify_signature(message, self.app_secret, message_dict["signature"]["HMAC"]):
                    raise exceptions.InvalidSignatureError

                # process based on action
                action = message_dict['payload']['action']
                await self._handle_received_request(message_dict, action)

            gc.collect()

    def _raise_event(self, device_id, action, value=None, cause="PHYSICAL_INTERACTION", instance_id=None) -> None:
        """
         Queues an event to be sent to the server, representing a device state change.
        """
        if self.limiter.try_acquire() :
            response = self._get_event_json(action, device_id, value, cause, instance_id)
            self.log.info(f'Adding event: {response} to publish queue!')
            self.publish_queue.put(response)
        else:
            self.log.error("Rate limit excceded. Adjusted rate:{}".format(self.limiter.events_per_minute))

    def _send_power_state_event_callback(self, device_id:str, state: bool, cause="PHYSICAL_INTERACTION") -> None:
        """
        Sends a power state change event.
        """
        value = {"state" : "On" if state else "Off"}
        self._raise_event(device_id, SinricProConstants.SET_POWER_STATE, value, cause)

    def _send_power_level_callback(self, device_id:str, power_level: int, cause="PHYSICAL_INTERACTION") -> None:
        """
        Sends a power level change event.
        """
        value = {"powerLevel" : power_level}
        self._raise_event(device_id, SinricProConstants.SET_POWER_LEVEL, value, cause)

    def _send_brightness_event_callback(self, device_id:str, brightness: int, cause="PHYSICAL_INTERACTION") -> None:
        """
        Sends a brightness change event.
        """
        value = {"brightness" : brightness}
        self._raise_event(device_id, SinricProConstants.SET_BRIGHTNESS, value, cause)

    def _send_change_channel_event_callback(self, device_id:str, channel_name: str, cause="PHYSICAL_INTERACTION") -> None:
        """
        Sends a channel change event.
        """
        value = {"channel": { "name": channel_name }}
        self._raise_event(device_id, SinricProConstants.CHANGE_CHANNEL, value, cause)

    def _send_color_event_callback(self, device_id:str, r: int, g: int, b: int, cause="PHYSICAL_INTERACTION") -> None:
        """
        Sends a color change event.
        """
        value = {"color": { "b": b, "g": g, "r": r }}
        self._raise_event(device_id, SinricProConstants.SET_COLOR, value, cause)

    def _send_color_temperature_event_callback(self, device_id:str, color_temperature: int, cause="PHYSICAL_INTERACTION") -> None:
        """
        Sends a color temperature change event.
        """
        value = {"colorTemperature": color_temperature}
        self._raise_event(device_id, SinricProConstants.COLOR_TEMPERATURE, value, cause)

    def _send_contact_event_callback(self, device_id:str, detected: bool, cause="PHYSICAL_INTERACTION") -> None:
        """
        Sends a contact sensor state change event.
        """
        value = {"state" : "open" if detected else "closed"}
        self._raise_event(device_id, SinricProConstants.SET_CONTACT_STATE, value, cause)

    def _send_door_state_event_callback(self, device_id:str, state: bool, cause="PHYSICAL_INTERACTION") -> None:
        """
        Sends a door state change event.
        """
        value = {"mode" : "Open" if state else "Close"}
        self._raise_event(device_id, SinricProConstants.SET_MODE, value, cause)

    def _send_doorbell_event_callback(self, device_id:str, cause="PHYSICAL_INTERACTION") -> None:
        """
        Sends doorbell state change event.
        """
        value = {"state" : "pressed" }
        self._raise_event(device_id, SinricProConstants.DOORBELLPRESS, value, cause)

    def _send_bands_event_callback(self, device_id:str, bands: str, level: int, cause="PHYSICAL_INTERACTION") -> None:
        """
        Sends bands (Speaker/TV) change event.
        """
        value = { "bands": [ { "value": level, "name": bands }] }
        self._raise_event(device_id, SinricProConstants.BANDS, value, cause)

    def _send_select_input_event_callback(self, device_id:str, intput: str, cause="PHYSICAL_INTERACTION") -> None:
        """
        Sends input state change event.
        """
        value = { "input": intput }
        self._raise_event(device_id, SinricProConstants.INPUT, value, cause)

    def _send_lock_state_event_callback(self, device_id:str, state: bool, cause="PHYSICAL_INTERACTION") -> None:
        """
        Sends lock state change event.
        """
        value = {"state" : "LOCKED" if state else "UNLOCKED"}
        self._raise_event(device_id, SinricProConstants.SET_LOCK_STATE, value, cause)

    def _send_media_control_event_callback(self, device_id:str, media_control: str, cause="PHYSICAL_INTERACTION") -> None:
        """
        Sends media control state change event.
        """
        value = {"control" : media_control}
        self._raise_event(device_id, SinricProConstants.MEDIA_CONTROL, value, cause)

    def _send_mode_event_callback(self, device_id:str, instance_id: str, mode: str, cause="PHYSICAL_INTERACTION") -> None:
        """
        Sends mode change event.
        """
        value = {"mode" : mode}
        self._raise_event(device_id, SinricProConstants.SET_MODE, value, cause, instance_id)

    def _send_motion_event_callback(self, device_id:str, detected: bool, cause="PHYSICAL_INTERACTION") -> None:
        """
        Sends motion detected/not-detected change event.
        """
        value = {"state" : "detected" if detected else "notDetected"}
        self._raise_event(device_id, SinricProConstants.MOTION, value, cause)

    def _send_mute_event_callback(self, device_id:str, mute: bool, cause="PHYSICAL_INTERACTION") -> None:
        """
        Sends mute event.
        """
        value = {"mute" : mute}
        self._raise_event(device_id, SinricProConstants.SET_MUTE, value, cause)

    def _set_percentage_event_callback(self, device_id:str, percentage: int, cause="PHYSICAL_INTERACTION") -> None:
        """
        Sends precentage change event.
        """
        value = {"percentage" : percentage}
        self._raise_event(device_id, SinricProConstants.SET_PRECENTAGE, value, cause)

    def _send_power_sensor_event_callback(self, device_id:str, start_time: int, voltage: float, current: float, power: float = -1.0,
                                          apparent_power: float = -1.0, reactive_power: float = -1.0, factor: float = -1.0,
                                          cause="PHYSICAL_INTERACTION") -> None:
        """
        Sends power consumption event.
        """
        value = {
            "startTime": start_time,
            "voltage": voltage,
            "current": current,
            "power": power,
            "apparentPower": apparent_power,
            "reactivePower": reactive_power,
            "factor": factor
        }
        self._raise_event(device_id, SinricProConstants.POWER_USAGE, value, cause)

    def _send_push_notification_event_callback(self, device_id: str, notification: str, cause="PHYSICAL_INTERACTION") -> None:
        """
        Sends push notification event.
        """
        value = {"notification": notification}
        self._raise_event(device_id, SinricProConstants.PUSH_NOTIFICATION, value, cause)

    def _send_range_value_event_callback(self, device_id: str, instance: str, range_value, cause="PHYSICAL_INTERACTION") -> None:
        """
        Sends numeric value change event.
        """
        value = {"rangeValue": range_value}
        self._raise_event(device_id, SinricProConstants.SET_RANGE_VALUE, value, cause, instance)

    def _send_temperature_event_callback(self, device_id: str, temperature: float, humidity: float = -1, cause="PHYSICAL_INTERACTION") -> None:
        """
        Sends temperature change event.
        """
        value = {"humidity": humidity, "temperature": temperature}
        self._raise_event(device_id, SinricProConstants.CURRENT_TEMPERATURE, value, cause)

    def _send_thermostat_mode_event_callback(self, device_id: str, thermostat_mode: str, cause="PHYSICAL_INTERACTION") -> None:
        """
        Sends thermostat mode event.
        """
        value = {"thermostatMode": thermostat_mode }
        self._raise_event(device_id, SinricProConstants.SET_THERMOSTAT_MODE, value, cause)

    def _send_target_temperature_event_callback(self, device_id: str, temperature: float, cause="PHYSICAL_INTERACTION") -> None:
        """
        Sends termostat or ac unit target temperature change.
        """
        value = {"temperature": temperature}
        self._raise_event(device_id, SinricProConstants.TARGET_TEMPERATURE, value, cause)

    def _send_toggle_state_event_callback(self, device_id: str, instance: str, state: bool, cause="PHYSICAL_INTERACTION") -> None:
        """
        Sends toggle state change event.
        """
        value = {"state" : "On" if state else "Off"}
        self._raise_event(device_id, SinricProConstants.SET_TOGGLE_STATE, value, cause, instance)

    def _send_volume_event_callback(self, device_id: str, volume: int, cause="PHYSICAL_INTERACTION") -> None:
        """
        Sends volume change event.
        """
        value = {"volume" : volume}
        self._raise_event(device_id, SinricProConstants.SET_TOGGLE_STATE, value, cause)


    def start(self, app_key, app_secret,*, server_url = "ws://ws.sinric.pro:80", restore_device_states = False, enable_log=False,) -> None:
        """
        Connect to SinricPro server and starts listening to commands.
        """

        if is_null_or_empty(app_key):
            raise exceptions.InvalidAppKeyError

        if is_null_or_empty(app_secret):
            raise exceptions.InvalidAppSecretError

        self.app_key = app_key
        self.app_secret = app_secret
        self.server_url = server_url
        self.restore_device_states = restore_device_states
        self.enable_log = enable_log

        # hook events
        for device in self.devices:
            if isinstance(device, PowerStateController):
                device.set_send_power_state_event_callback(self._send_power_state_event_callback)
            elif isinstance(device, PowerLevelController):
                device.set_send_power_level_event_callback(self._send_power_level_callback)
            elif isinstance(device, BrightnessController):
                device.set_send_brightness_event_callback(self._send_brightness_event_callback)
            elif isinstance(device, ChannelController):
                device.set_send_change_channel_event_callback(self._send_change_channel_event_callback)
            elif isinstance(device, ColorController):
                device.set_send_color_event_callback(self._send_color_event_callback)
            elif isinstance(device, ColorTemperatureController):
                device.send_color_temperature_event_callback(self._send_color_temperature_event_callback)
            elif isinstance(device, ContactSensor):
                device.set_send_contact_event_callback(self._send_contact_event_callback)
            elif isinstance(device, DoorController):
                device.set_send_door_state_event_callback(self._send_door_state_event_callback)
            elif isinstance(device, Doorbell):
                device.set_send_doorbell_event_callback(self._send_doorbell_event_callback)
            elif isinstance(device, EqualizerController):
                device.set_send_bands_event_callback(self._send_bands_event_callback)
            elif isinstance(device, InputController):
                device.set_send_select_input_event_callback(self._send_select_input_event_callback)
            elif isinstance(device, LockController):
                device.set_send_lock_state_event_callback(self._send_lock_state_event_callback)
            elif isinstance(device, MediaController):
                device.set_send_media_control_event_callback(self._send_media_control_event_callback)
            elif isinstance(device, ModeController):
                device.set_send_mode_event_callback(self._send_mode_event_callback)
            elif isinstance(device, MotionSensor):
                device.set_send_motion_event_callback(self._send_motion_event_callback)
            elif isinstance(device, MuteController):
                device.set_send_mute_event_callback(self._send_mute_event_callback)
            elif isinstance(device, PercentageController):
                device.set_send_set_percentage_event_callback(self._set_percentage_event_callback)
            elif isinstance(device, PowerSensor):
                device.set_send_power_sensor_event_callback(self._send_power_sensor_event_callback)
            elif isinstance(device, PushNotificationController):
                device.set_send_push_notification_event_callback(self._send_push_notification_event_callback)
            elif isinstance(device, RangeController):
                device.set_send_range_value_event_callback(self._send_range_value_event_callback)
            elif isinstance(device, TemperatureSensor):
                device.set_send_temperature_event_callback(self._send_temperature_event_callback)
            elif isinstance(device, ThermostatController):
                device.set_send_thermostat_mode_event_callback(self._send_thermostat_mode_event_callback)
                device.set_send_target_temperature_event_callback(self._send_target_temperature_event_callback)
            elif isinstance(device, ToggleController):
                device.set_send_toggle_state_event_callback(self._send_toggle_state_event_callback)
            elif isinstance(device, VolumeController):
                device.set_send_volume_event(self._send_volume_event_callback)

        if self.enable_log :
            self.log.level  = DEBUG
        else:
            self.log.level  = ERROR

        uasyncio.create_task(self._connect())
        uasyncio.create_task(self._process_received_queue())
        uasyncio.create_task(self._process_publish_queue())
