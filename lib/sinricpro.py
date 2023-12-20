from async_websocket_client import AsyncWebsocketClient
from async_queue import AsyncQueue
from lib.exceptions import exceptions
from lib.sinricpro_constants import SinricProConstants
from lib.utils.generic import is_null_or_empty
from lib.utils.signer import Signer
import uasyncio
import json
import gc

class SinricPro:
    def __init__(self):
        self.devices = []
        self.ws = AsyncWebsocketClient() # create instance of websocket
        self.publish_queue = AsyncQueue(5) # create publish queue
        self.received_queue = AsyncQueue(5) # create publish queue
        self.signer = Signer()

    def add_device(self, device) -> None:
        self.devices.append(device)

    async def _connect(self) -> None:
        # setup device ids
        device_ids = []         
        for device in self.devices:
            device_ids.append(device.device_id)
            if self.enable_log : print(f"Adding {device.device_id}.")
        
        # setup websocket headers
        headers = []
        headers.append(("appkey", self.app_key))
        headers.append(("deviceids", ';'.join(device_ids)))

        if self.enable_log : print("Connecting...")

        # connect to SinricPro websocket server        
        if not await self.ws.handshake(self.server_url, headers=headers):
            raise RuntimeError("Cannot connect to SinricPro server!.")
        
        if self.enable_log : print("Connected to SinricPro server!")

        while await self.ws.open():
            data = await self.ws.recv()
            if self.enable_log : print('<-', str(data))
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

    async def _handle_set_power_state(self, message_dict):
        #try:
        target_device_id = message_dict['payload']['deviceId']
        state = message_dict['payload']['value']['state']

        # look for the device id and invoke the callback
        for device in self.devices:
            if device.device_id == target_device_id :
                success = await device.power_state_callback(target_device_id, state)
                value_dict = message_dict['payload']['value']
                response = self._get_response_json(message_dict=message_dict, success=success, value_dict=value_dict, instance_id=None)
                self.publish_queue.put(response)

        # except Exception as e:
        #     print(f'Error : {e}')

    async def _process_publish_queue(self) -> None:
        async for message in self.publish_queue:
            if self.enable_log : print(f'-> : {message}')
            await self.ws.send(message)

    async def _process_received_queue(self) -> None:
        async for message in self.received_queue:
            message_dict = json.loads(message)
            
            if "timestamp" in message_dict:
                if self.enable_log : print("Got TimeStamp!")
            else:
                # verify signature
                if not self.signer.verify_signature(message, self.app_secret, message_dict["signature"]["HMAC"]):
                    raise exceptions.InvalidSignatureError

                action = message_dict['payload']['action']

                if action == SinricProConstants.SET_POWER_STATE:
                    await self._handle_set_power_state(message_dict)

            gc.collect()
 
    def start(self, app_key, app_secret, server_url = "ws://ws.sinric.pro:80", restoredevicestates = False, enable_log=False,) -> None:
        if is_null_or_empty(app_key):
            raise exceptions.InvalidAppKeyError

        if is_null_or_empty(app_secret):
            raise exceptions.InvalidAppSecretError

        self.app_key = app_key
        self.app_secret = app_secret
        self.server_url = server_url
        self.restoredevicestates = restoredevicestates
        self.enable_log = enable_log

        if self.enable_log : print("Start SinricPro..")

        uasyncio.create_task(self._connect())
        uasyncio.create_task(self._process_received_queue())
        uasyncio.create_task(self._process_publish_queue())