import django_filters
from django.forms import DateInput
from django_filters import filters

from shop.models import Sale


class StockFilter(django_filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr='icontains')
    create__gte = filters.DateTimeFilter(field_name="create",
                                             lookup_expr='date__gte',
                                             widget=DateInput(attrs={'type': 'date'}))
    create__lte = filters.DateTimeFilter(field_name="create",
                                             lookup_expr='date__lte',
                                             widget=DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Sale
        fields = ['name', 'create__gte', 'create__lte']