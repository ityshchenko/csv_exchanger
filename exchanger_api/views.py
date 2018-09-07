from django_filters.rest_framework import (
    DjangoFilterBackend,
)

from iso4217 import Currency

from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.serializers import (
    Field,
    HyperlinkedModelSerializer,
    SerializerMethodField,
    Serializer,
)
from rest_framework.viewsets import ModelViewSet

from .models import (
    CH_ORDER_STATE,
    CH_ORDER_TYPES,
    Order,
    Merchant,
)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class MerchantSerializer(Serializer):
    id = Field(source='pk_id')

    class Meta:
        model = Merchant
        fields = ('id', )


class MerchantViewSet(ModelViewSet):
    queryset = Merchant.objects.all()
    serializer_class = MerchantSerializer
    pagination_class = StandardResultsSetPagination


class OrderSerializer(HyperlinkedModelSerializer):
    currency = SerializerMethodField('get_currency_name')
    ord_type = SerializerMethodField('get_ord_type_name')
    status = SerializerMethodField('get_status_name')

    @staticmethod
    def get_currency_name(obj):
        return list(
            filter(lambda c: c.number == obj.currency, Currency)
        )[0].name

    def get_ord_type_name(self, obj):
        return CH_ORDER_TYPES[obj.ord_type - 1][1]

    def get_status_name(self, obj):
        return CH_ORDER_STATE[obj.status - 1][1]

    class Meta:
        model = Order
        fields = (
            'pk_id',
            'amount',
            'currency',
            'creation_time',
            'merchant',
            'merchant_id',
            'ord_type',
            'readable_id',
            'status',
            'description',
        )


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )
    filter_fields = ('pk_id', )
    search_fields = ('description', )
    ordering_fields = ('amount', 'created_at', 'ord_type', 'status', )
    ordering = ('-creation_time', )