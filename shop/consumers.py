# from channels.consumer import SyncConsumer, AsyncConsumer
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer


class MySyncConsumer(WebsocketConsumer):
    def connect(self, event):
        print("websocket connected successfully...", event)
        # Accept the connection
        self.send({
            "type": "websocket.accept"
        })

    def receive(self, event):
        print("WebSocket received...", event)

    def disconnect(self, event):
        print("WebSocket disconnected...", event)

    
import json
class MyAsyncConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Accept first
        await self.accept()

        # Now you can safely send
        await self.send(text_data=json.dumps({"message": "WebSocket connected successfully"}))

    async def disconnect(self, close_code):
        print("Disconnected:", close_code)

    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.send(text_data=json.dumps({"echo": data}))