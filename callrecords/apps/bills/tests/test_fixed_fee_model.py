import pytest
from apps.bills.models import FixedFee
from django.db import models
from django.utils.dateparse import parse_time
from tests.factories import FixedFeeFactory

pytestmark = pytest.mark.django_db(transaction=True)


def test_create_new_fixed_fee():
    fixed_fee = FixedFee.objects.create(start=parse_time('06:00:00'), end=parse_time('22:00:00'), price=0.09)

    assert fixed_fee is not None
    assert fixed_fee.start == parse_time('06:00:00')
    assert fixed_fee.price == 0.09


def test_get_fixed_fee_created():
    fixed_fee = FixedFeeFactory()
    fee = FixedFee.objects.get(pk=fixed_fee.pk)

    assert fixed_fee == fee


def test_get_not_existing_model_fixed_fee():
    fixed_fee = FixedFeeFactory()

    try:
        fixed_fee = FixedFee.objects.get(pk=fixed_fee.pk + 1)
    except models.ObjectDoesNotExist:
        fixed_fee = None

    assert fixed_fee is None
