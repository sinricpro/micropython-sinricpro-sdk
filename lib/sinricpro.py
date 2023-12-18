from async_websocket_client import AsyncWebsocketClient
from async_queue import AsyncQueue
import uasyncio
import json
import gc

class SinricPro:
    def __init__(self):
        self.devices = []
        self.ws = AsyncWebsocketClient() # create instance of websocket
        self.publish_queue = AsyncQueue(5) # create publish queue
        self.received_queue = AsyncQueue(5) # create publish queue

    def add_device(self, device) -> None:
        self.devices.append(device)

    async def connect(self) -> None:
        # setup device ids
        device_ids = []         
        for device in self.devices:
            device_ids.append(device.device_id)
            print(f"Adding {device.device_id}.")
        
        # setup websocket headers
        headers = []
        headers.append(("appkey", self.app_key))
        headers.append(("deviceids", ';'.join(device_ids)))

        print("Connecting...")

        # connect to SinricPro websocket server        
        if not await self.ws.handshake(self.server_url, headers=headers):
            raise RuntimeError("Cannot connect to SinricPro server!.")
        
        print("Connected to SinricPro server!")

        while await self.ws.open():
            data = await self.ws.recv()
            self.received_queue.put(str(data))
            gc.collect()

    async def process_received_queue(self) -> None:
        async for message in self.received_queue:
            print('<-', message)
            message_dict = json.loads(message)
            
            if message_dict["timestamp"]:
                print("Got TimeStamp!")
            else:
                print("Do something with this")

            gc.collect()

    def begin(self, app_key, app_secret, server_url = "ws://ws.sinric.pro:80", restoredevicestates = False) -> None:
        print("Begin SinricPro..")

        self.app_key = app_key
        self.app_secret = app_secret
        self.server_url = server_url
        self.restoredevicestates = restoredevicestates

        uasyncio.create_task(self.connect())
        uasyncio.create_task(self.process_received_queue())
        #uasyncio.create_task(self.process_publish_queue())