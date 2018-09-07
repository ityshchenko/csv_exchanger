from dataclasses import dataclass, field, asdict
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError
from django.db.transaction import atomic
from iso4217 import Currency

import csv
import requests

from exchanger_api.models import (
    CH_ORDER_STATE,
    CH_ORDER_TYPES,
    Merchant,
    Order,
)


# Order is important
@dataclass
class OrderType:
    pk_id: int
    __creation_time: str
    merchant_id: int
    __status: str
    __amount: str
    __currency: str
    readable_id: str
    __ord_type: int
    description: str

    amount: float = field(init=False)
    creation_time: datetime = field(init=False)
    status: int = field(init=False)
    currency: int = field(init=False)
    ord_type: int = field(init=False)

    def __post_init__(self):
        self.creation_time = \
            datetime.strptime(self.__creation_time, '%d.%m.%y %H:%M:%S')
        self.amount = float(self.__amount.replace(',', '.'))
        self.status = \
            [*filter(lambda x: self.__status in x, CH_ORDER_STATE)][0][0]
        self.currency = \
            Currency(self.__currency).number
        self.ord_type = \
            [*filter(lambda x: self.__ord_type in x, CH_ORDER_TYPES)][0][0]

    def __dir__(self):
        return filter(
            lambda k: not k.startswith(f'_{self.__class__.__name__}__'),
            self.__dict__.keys()
        )


class Command(BaseCommand):
    args = 'url to file.csv or path'
    help = 'patch to current database'

    @staticmethod
    def patch_db(source):
        for row in source:
            o = OrderType(*row)
            merchant, s = Merchant.objects.get_or_create(pk=o.merchant_id)
            if s:
                merchant.save()
            opts = {k: v for k, v in vars(o).items() if '__' not in k}
            try:
                order = Order.objects.get(pk_id=o.pk_id)
                for k, v in opts.items():
                    setattr(order, k, v)
            except ObjectDoesNotExist:
                order = Order(**opts)
            order.save()

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)
        parser.add_argument('newline', nargs='?', type=str)

    def handle(self, *args, **options):
        _path = options.get('path')
        _newline = options.get('newline') or '\n'

        if not _path:
            raise CommandError('Path is required.\n\nEnter path or url to csv-file.')

        try:
            if _path.startswith('http://') or \
                    _path.startswith('https://'):
                r = requests.get(_path)
                if not r.status_code == 200:
                    raise CommandError('Source error\n\nCheck source')
                f = r.content.decode('utf-8').splitlines()[1:]
                spam_reader = csv.reader(f, )

                with atomic():
                    self.patch_db(spam_reader)

                return
            with open(_path, newline=_newline) as f:
                f.readline()
                spam_reader = csv.reader(f, )

                with atomic():
                    self.patch_db(spam_reader)
        except DatabaseError as ex:
            raise CommandError(f"Rollback...\n{ex}")