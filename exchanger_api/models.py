from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from datetime import datetime

from iso4217 import Currency

# Create your models here.


CH_ORDER_STATE = [
    (1, 'approved'),
    (2, 'declined'),
    (3, 'expired'),
    (4, 'processing'),
    (5, 'reversed'),
]


CH_ORDER_TYPES = [
    (1, 'verification'),
    (2, 'purchase'),
]


def check_currency(value):
    """
    Check currency in ISO4712
    :param value:
    :return:
    """
    try:
        if value is int:
            assert isinstance(
                filter(lambda c: c.number == value, Currency)[-1],
                Currency
            )
        else:
            Currency(value)
    except (AssertionError, KeyError, ValueError, ):
        raise ValidationError(
            _('%(value)s is not valid currency'),
            params={'value': value},
        )


def check_amount_order(val):
    if round(val) <= 0.0:
        raise ValidationError(
            _('%(value)s less or equal zero.'),
            params={'value': val}
        )


def timestamp_now():
    return datetime.now().timestamp()


class Merchant(models.Model):
    pk_id = models.BigIntegerField(primary_key=True)
    # TODO: Merchant models

    def __str__(self):
        return self.pk_id


class Order(models.Model):
    pk_id = models.BigIntegerField(primary_key=True)

    creation_time = models.DateTimeField(
        null=False,
        default=timestamp_now,
    )

    merchant = models.ForeignKey(
        'Merchant',
        null=False,
        on_delete=models.PROTECT
    )

    status = models.IntegerField(choices=CH_ORDER_STATE, null=False)

    amount = models.FloatField(
        validators=[check_amount_order],
        null=False
    )
    currency = models.DecimalField(
        max_digits=3,
        decimal_places=0,
        validators=[check_currency]
    )

    readable_id = models.CharField(max_length=256, null=False)

    ord_type = models.IntegerField(choices=CH_ORDER_TYPES, null=False)

    description = models.CharField(max_length=500)
