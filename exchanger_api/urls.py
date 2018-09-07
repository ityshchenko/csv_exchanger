from django.urls import path, include
from rest_framework import routers

from .views import MerchantViewSet, OrderViewSet


router = routers.DefaultRouter()
router.register('merchants', MerchantViewSet)
router.register('orders', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
