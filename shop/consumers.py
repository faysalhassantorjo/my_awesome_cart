from channels.consumer import SyncConsumer, AsyncConsumer


class MySyncConsumer(SyncConsumer):
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

    

class MyAsyncConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("websocket connected successfully...", event)
        await self.send({
            "type": "websocket.accept"
        })

    async def websocket_receive(self, event):
        print("WebSocket received...", event)

    async def websocket_disconnect(self, event):
        print("WebSocket disconnected...", event)

    