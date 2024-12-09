from django.db.models import Prefetch
from django.utils.decorators import method_decorator
from rest_framework import viewsets, permissions, status, response

from drf_yasg.utils import swagger_auto_schema
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError

from .models import Sale, Price, Goods, Order
from .permissions import IsStaffForPost
from .serializers import SaleListSerializer, SaleRetrieveSerializer, PriceListSerializer, PriceCreateSerializer, \
    GoodListSerializer, SaleGenerateSerializer, OrderListSerializer, SalePatchSerializer
from .filters import StockFilter
from .throttling import CreationPriceThrottle


@method_decorator(name='list', decorator=swagger_auto_schema(
        operation_description="Return only active sales. You can filter by date range or name",
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
        operation_description="Include all goods each was added in sale",
))
@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_description="Create Stock with min max price",
    request_body=SaleListSerializer,
))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(
    operation_description="Here you can add goods to stock",
    request_body=SalePatchSerializer,
))
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_description="Generate new price for each goods was added to stock",
    request_body=SaleGenerateSerializer,
))
class StockApiView(viewsets.ModelViewSet):
    queryset = Sale.objects.filter(is_active=True)
    permission_classes = [IsStaffForPost, permissions.IsAuthenticatedOrReadOnly]
    serializer_class = SaleListSerializer
    filter_backends = [DjangoFilterBackend,]
    filterset_class = StockFilter
    http_method_names = ['get', 'post', 'put', 'patch', 'options', 'head']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SaleRetrieveSerializer

        if self.request.method == 'PUT':
            return SaleGenerateSerializer

        if self.request.method == 'PATCH':
            return SalePatchSerializer

        return SaleListSerializer

    def get_throttles(self):
        if self.request.method == 'PUT':
            return [CreationPriceThrottle('PUT')]
        return super().get_throttles()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.update_price()
        response_text = list(instance.goods.all().values_list('name', flat=True))
        return response.Response(status=status.HTTP_200_OK, data={'price_update_for': response_text})

    def partial_update(self, request, *args, **kwargs):
        gd = request.data.get('goods')
        if not isinstance(gd, list):
            if isinstance(gd, int):
                gd = [gd]
            else:
                raise ValidationError('Value must be integer or list of integers')

        goods_data = Goods.objects.filter(pk__in=gd, is_active=True)
        if goods_data.count() == 0:
            return response.Response(status=status.HTTP_400_BAD_REQUEST)

        instance = self.get_object()
        response_text = []
        if goods_data:
            instance.goods.add(*goods_data)
            instance.save()
            response_text = list(instance.goods.all().values_list('name', flat=True))
        return response.Response(data={'goods_add': response_text}, status=status.HTTP_202_ACCEPTED)

    def retrieve(self, request, *args, **kwargs):
        self.queryset = Sale.objects.filter(pk=self.kwargs['pk']).prefetch_related(
            Prefetch('goods', queryset=Goods.objects.all())
        )
        return super().retrieve(request, *args, **kwargs)


class PriceApiView(viewsets.ModelViewSet):
    queryset = Price.objects.filter(is_active=True)
    permission_classes = [IsStaffForPost, permissions.IsAuthenticatedOrReadOnly]
    serializer_class = PriceListSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return PriceCreateSerializer
        return PriceListSerializer


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description="Only for authorized user. \nReturn list the orders of current user",
))
class GoodsApiView(viewsets.ModelViewSet):
    queryset = Goods.objects.all()
    permission_classes = [IsStaffForPost, permissions.IsAuthenticatedOrReadOnly]
    serializer_class = GoodListSerializer
    filter_backends = [DjangoFilterBackend,]
    filterset_fields = ['is_active',]
    http_method_names = ['get', 'head', 'options', 'trace']


    def get_queryset(self):
        if self.action == 'retrieve':
            return Goods.objects.filter(is_active=True).prefetch_related(
                Prefetch('prices', queryset=Price.objects.all())
            )

        return Goods.objects.filter(is_active=True).prefetch_related(
                    Prefetch('prices', queryset=Price.objects.filter(is_active=True))
                )



@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description="Only for authorized user. \nReturn list the orders of current user",
))
@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_description="Only for authorized user. \nTo place an order, provide the product ID and quantity. "
                          "\nIf the product is on sale, the applicable sale price at the time of the "
                          "order will be used.",
    request_body=OrderListSerializer,
))
class OrdersApiViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderListSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'head', 'options', 'trace']

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
