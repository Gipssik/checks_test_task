import datetime
from typing import Optional

from fastapi_filter import FilterDepends
from fastapi_filter.contrib.sqlalchemy import Filter

from checks_test_task.conf.constants import PaymentType
from checks_test_task.models import Check, Payment


class PaymentFilter(Filter):
    payment_type: Optional[PaymentType] = None

    class Constants(Filter.Constants):
        model = Payment


class CheckFilter(Filter):
    created_at__gte: Optional[datetime.datetime] = None
    created_at__lte: Optional[datetime.datetime] = None
    total_price__gte: Optional[float] = None
    total_price__lte: Optional[float] = None
    rest__gte: Optional[float] = None
    rest__lte: Optional[float] = None
    payment: Optional[PaymentFilter] = FilterDepends(PaymentFilter)

    class Constants(Filter.Constants):
        model = Check
