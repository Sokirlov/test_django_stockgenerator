from collections import OrderedDict

from rest_framework import serializers
from shop_settings.models import Currency
from shop_settings.serializers import CurrencySerializer
from .models import Sale, Price, Goods, Order


class PriceCreateSerializer(serializers.ModelSerializer):
    currency = serializers.PrimaryKeyRelatedField(queryset=Currency.objects.filter(is_active=True))
    goods = serializers.PrimaryKeyRelatedField(queryset=Goods.objects.filter(is_active=True))

    class Meta:
        model = Price
        fields = ['currency', 'goods', 'base_price']

    def to_representation(self, instance):
        """ Update view to show more data about instance"""
        ordered_representation = OrderedDict([
            ('id', instance.id),
            ('amount', instance.base_price),
            ('price', instance.price_in_currency),
            ('currency', CurrencySerializer(instance.currency).data),
            ('is_active', instance.is_active),
            ('stock_id', instance.goods.id),
            ('stock_name', instance.goods.name),
        ])
        return ordered_representation


class PriceListSerializer(serializers.ModelSerializer):
    create = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    update = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    price = serializers.SerializerMethodField()
    goods = serializers.StringRelatedField(many=False, read_only=True)
    currency = CurrencySerializer(read_only=False)

    class Meta:
        model = Price
        fields = ['id', 'is_active', 'goods', 'price', 'base_price', 'currency',
                  'create', 'update', 'create_by', 'update_by']

    @staticmethod
    def get_price(obj):
        """
        return price in current currency, generated with exchange_rate value
        """
        return obj.price_in_currency


class GoodListSerializer(serializers.ModelSerializer):
    prices = PriceListSerializer(read_only=True, many=True)
    create = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    update = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    create_by = serializers.StringRelatedField(read_only=True)
    update_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Goods
        fields = ['id', 'name', 'create', 'update', 'create_by', 'update_by', 'prices',]


class StockSerializer(serializers.ModelSerializer):
    min_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    max_price = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Sale
        fields = ['id', 'name', 'min_price', 'max_price',]


class SalePatchSerializer(serializers.ModelSerializer):
    goods = serializers.PrimaryKeyRelatedField(queryset=Goods.objects.filter(is_active=True), many=True, required=False)

    class Meta:
        model = Sale
        fields = ['goods',]


class SaleListSerializer(StockSerializer):
    create = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    update = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    create_by = serializers.StringRelatedField(read_only=True)
    update_by = serializers.StringRelatedField(read_only=True)

    class Meta(StockSerializer.Meta):
        model = Sale
        fields = StockSerializer.Meta.fields + ['create', 'update', 'create_by', 'update_by']


class SaleRetrieveSerializer(SaleListSerializer):
    goods = GoodListSerializer(many=True, read_only=True)

    class Meta(SaleListSerializer.Meta):
        fields = SaleListSerializer.Meta.fields + ['goods']


class SaleGenerateSerializer(serializers.ModelSerializer):
    """
        Serializer for creating random Price for attached Goods
    """
    class Meta:
        model = Sale
        fields = ['id']


class OrderListSerializer(serializers.ModelSerializer):
    price = serializers.ReadOnlyField(source='order.price')
    order_sum = serializers.ReadOnlyField(source='order.order_sum')
    status = serializers.ReadOnlyField(source='order.status')

    class Meta:
        model = Order
        fields = ['id', 'goods', 'price', 'amount', 'order_sum', 'status']

    def validate(self, attrs):
        attrs['user'] = self.context['request'].user
        attrs['price'] = Price.objects.get(goods=attrs['goods'], is_active=True)
        return attrs