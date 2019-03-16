import pytest
from django.db import models
from apps.calls.models import CallStart
from tests.factories import CallStartFactory
from django.utils.dateparse import parse_datetime

pytestmark = pytest.mark.django_db(transaction=True)


def test_create_new_model_call_start():
    call_start = CallStart.objects.create(
        id=1,
        source=41997020434,
        destination=44992782462,
        timestamp=parse_datetime('2016-02-29T12:00:00Z')
    )

    assert call_start is not None
    assert call_start.id == 1
    assert call_start.source == 41997020434


def test_get_model_call_start_created():
    call = CallStartFactory()

    call_start = CallStart.objects.get(id=call.id)

    assert call == call_start


def test_get_not_existing_model_call_start():
    call = CallStartFactory()

    try:
        call_start = CallStart.objects.get(pk=call.id + 1)
    except models.ObjectDoesNotExist:
        call_start = None

    assert call_start is None
