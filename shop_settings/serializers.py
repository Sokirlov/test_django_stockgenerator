import html
from rest_framework import serializers

from shop_settings.models import Currency


class CurrencySerializer(serializers.ModelSerializer):
    symbol = serializers.SerializerMethodField()

    class Meta:
        model = Currency
        fields = ['id', 'name', 'iso_code', 'symbol', 'exchange_rate', 'is_active']

    @staticmethod
    def get_symbol(obj):
        return html.unescape(obj.symbol)
