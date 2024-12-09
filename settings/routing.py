from django.urls import path
from shop.consumers import PriceConsumer

websocket_urlpatterns = [
    path('ws/price_updates/', PriceConsumer.as_asgi()),
]
