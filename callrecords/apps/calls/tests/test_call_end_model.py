import pytest
from django.db import models
from apps.calls.models import CallEnd
from tests.factories import CallEndFactory
from django.utils.dateparse import parse_datetime


pytestmark = pytest.mark.django_db(transaction=True)


def test_create_new_model_call_end():
    call_end = CallEnd.objects.create(
        id=25,
        timestamp=parse_datetime('2016-02-29T12:00:00Z'),
    )
    assert call_end is not None
    assert call_end.id == 25


def test_get_model_call_end_created():
    call = CallEndFactory()
    call_end = CallEnd.objects.get(pk=call.pk)

    assert call_end.id == call.id
    assert call_end is not None


def test_get_not_existing_model_call_end():
    call = CallEndFactory()

    try:
        call = CallEnd.objects.get(id=call.pk + 1)
    except models.ObjectDoesNotExist:
        call = None

    assert call is None
