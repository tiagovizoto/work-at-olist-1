import pytest
from apps.bills.models import MinuteFee
from django.db import models
from django.utils.dateparse import parse_time
from tests.factories import MinuteFeeFactory

pytestmark = pytest.mark.django_db(transaction=True)


def test_create_new_minute_fee():
    minute_fee = MinuteFee.objects.create(start=parse_time('06:00:00'), end=parse_time('22:00:00'), price=0.09)

    assert minute_fee is not None
    assert minute_fee.start == parse_time('06:00:00')
    assert minute_fee.price == 0.09


def test_get_minute_fee_created():
    minute_fee = MinuteFeeFactory()
    fee = MinuteFee.objects.get(pk=minute_fee.pk)

    assert minute_fee == fee


def test_get_not_existing_model_minute_fee():
    minute_fee = MinuteFeeFactory()

    try:
        minute_fee = MinuteFee.objects.get(pk=minute_fee.pk + 1)
    except models.ObjectDoesNotExist:
        minute_fee = None

    assert minute_fee is None
