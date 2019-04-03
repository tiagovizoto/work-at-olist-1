import pytest
from apps.bills.models import Bill
from django.db import models
from tests.factories import FixedFeeFactory, BillFactory, CallStartFactory, CallEndFactory


pytestmark = pytest.mark.django_db(transaction=True)


def test_create_new_bill():
    fixed_fee = FixedFeeFactory()
    call_start = CallStartFactory()
    call_end = CallEndFactory()

    bill = Bill.objects.create(
        price=35.01,
        fixed_fee=fixed_fee,
        call_start=call_start,
        call_end=call_end
    )

    assert bill is not None


def test_get_bill_created():
    bill = BillFactory()
    bill_get = Bill.objects.get(pk=bill.pk)

    assert bill == bill_get


def test_get_not_existing_model_bill():
    bill = BillFactory()

    try:
        bill = Bill.objects.get(pk=bill.pk + 1)
    except models.ObjectDoesNotExist:
        bill = None

    assert bill is None
