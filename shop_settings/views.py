from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from shop_settings.models import Currency
from shop_settings.serializers import CurrencySerializer


class CurrencyApiView(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    filter_backends = [DjangoFilterBackend,]
    filterset_fields = ['name', 'iso_code', 'is_active',]
    http_method_names = ['get', 'head', 'options', 'trace']
