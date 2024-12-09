from django.urls import include, path
from rest_framework import routers

from shop_settings.views import CurrencyApiView
from .views import StockApiView, PriceApiView, GoodsApiView, OrdersApiViewSet

router = routers.DefaultRouter()
router.register('currency', CurrencyApiView)
router.register('goods', GoodsApiView)
router.register('prices', PriceApiView)
router.register('sales', StockApiView)
router.register('orders', OrdersApiViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
