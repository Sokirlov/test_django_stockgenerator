import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer

class PriceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'prices'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_price_update(self, event):
        await self.send(text_data=json.dumps(event['data']))


def broadcast_price_update(price_instance):
    channel_layer = get_channel_layer()
    data = {
        "goods": price_instance.goods.name,
        "price": str(price_instance.base_price),
    }

    async_to_sync(channel_layer.group_send)(
        "prices",
        {
            "type": "send_price_update",
            "data": data,
        }
    )