from django_filters.rest_framework import (
    DjangoFilterBackend,
)

from iso4217 import Currency

from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.serializers import Serializer, Field
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


