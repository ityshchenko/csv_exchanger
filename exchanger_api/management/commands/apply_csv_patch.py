from dataclasses import dataclass, field, asdict
from datetime import datetime
from iso4217 import Currency

from exchanger_api.models import (
    CH_ORDER_STATE,
    CH_ORDER_TYPES,
)


# Order is important
@dataclass
class Order:
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


