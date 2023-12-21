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

class SinricPro:
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
        self.devices.append(device)

    async def _connect(self) -> None:
        # setup device ids
        device_ids = []
        for device in self.devices:
            device_ids.append(device.device_id)
            if self.enable_log :
                self.log.debug(f"Adding {device.device_id}.")

        # setup websocket headers
        headers = []
        headers.append(("appkey", self.app_key))
        headers.append(("deviceids", ';'.join(device_ids)))
        headers.append(("platform", 'micropython'))
        headers.append(('restoredevicestates', ('true' if self.restore_device_states else 'false')))
        headers.append(("sdkversion", self.sdkversion))

        if self.enable_log :
            self.log.debug(f"Connecting to {self.server_url}")

        # connect to SinricPro websocket server
        if not await self.ws.handshake(self.server_url, headers=headers):
            self.log.error("Connection failed!")
            raise RuntimeError("Cannot connect to SinricPro server!.")

        if self.enable_log :
            self.log.debug("Connected!")

        while await self.ws.open():
            data = await self.ws.recv()
            if self.enable_log : 
                self.log.debug('<-{}'.format(str(data)))

            self.received_queue.put(str(data))
            gc.collect()

    def _get_response_json(self, message_dict, success, value_dict, instance_id='') -> str:
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

    def _get_event_json(self, action:str, device_id:str, value:str, type_of_interaction:str="PHYSICAL_INTERACTION") -> str:
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

        signature = self.signer.get_signature(self.app_secret, payload)
        return json.dumps( {"header": header, "payload": payload, "signature": signature} )

    async def _handle_set_power_state(self, message_dict):
        try:
            target_device_id = message_dict['payload']['deviceId']
            state = message_dict['payload']['value']['state']

            # look for the device id and invoke the callback
            for device in self.devices:
                if device.device_id == target_device_id :
                    success = await device.power_state_callback(target_device_id, state)
                    value_dict = message_dict['payload']['value']
                    response = self._get_response_json(message_dict=message_dict, success=success, value_dict=value_dict, instance_id=None)
                    self.publish_queue.put(response)

        except Exception as e:
            self.log.error(f'Error : {e}')

    async def _process_publish_queue(self) -> None:
        try:
            async for message in self.publish_queue:
                print("Got message!")
                if self.enable_log :
                    self.log.info('-> : {}'.format(message))
                await self.ws.send(message)
        except Exception as e:
            self.log.error(f'Error : {e}')

    async def _process_received_queue(self) -> None:
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

                if action == SinricProConstants.SET_POWER_STATE:
                    await self._handle_set_power_state(message_dict)

            gc.collect()

    def _raise_event(self, device_id, action, value=None, cause="PHYSICAL_INTERACTION"):
        if self.limiter.try_acquire() :
            if action == SinricProConstants.SET_POWER_STATE:
                response = self._get_event_json(action, device_id, value, cause)
                self.log.info(f'Adding event: {response} to publish queue!')
                self.publish_queue.put(response)
            else:
                self.log.error(f'action: {action} not supported!')
        else:
            self.log.error("Rate limit excceded. Adjusted rate:{}".format(self.limiter.events_per_minute))

    def _send_power_state_event_callback(self, device_id:str, state: bool, cause="PHYSICAL_INTERACTION"):
        self.log.info('Sending power state event')
        value = {"state" : "On" if state else "Off"}
        self._raise_event(device_id, SinricProConstants.SET_POWER_STATE, value, cause)


    def start(self, app_key, app_secret,*, server_url = "ws://ws.sinric.pro:80", restore_device_states = False, enable_log=False,) -> None:
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
                device.send_power_state_event_callback = self._send_power_state_event_callback

        if self.enable_log :
            self.log.level  = DEBUG
        else:
            self.log.level  = ERROR

        uasyncio.create_task(self._connect())
        uasyncio.create_task(self._process_received_queue())
        uasyncio.create_task(self._process_publish_queue())
