import pytest
from tests.factories import FixedFeeFactory
pytestmark = pytest.mark.django_db(transaction=True)


def test_post_fixed_fee(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {
        'price': 0.09,
        'start': '06:00:00',
        'end': '22:00:00'
    }

    rv = client.post('/v1/bill/fee/fixed/', data=data, headers=headers)
    assert rv.data is not None


def test_get_fixed_fee(client):
    fee = FixedFeeFactory()

    rv = client.get(f'/v1/bill/fee/fixed/{fee.id}/')
    assert rv.status_code == 200


def test_delete_fixed_fee(client):
    fee = FixedFeeFactory()
    rv = client.delete(f'/v1/bill/fee/fixed/{fee.id}/')
    assert rv.status_code == 204


def test_fail_put_fixed_fee(client):
    fee = FixedFeeFactory()

    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {
        'price': 0.36
    }

    rv = client.put(f'/v1/bill/fee/fixed/{fee.id}/', data=data, headers=headers)
    assert rv.status_code == 405


def test_post_fixed_fee_without_the_fields_start_and_end(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {
        'price': 0.36
    }

    rv = client.post('/v1/bill/fee/fixed/', data=data, headers=headers)
    assert rv.status_code == 400


def test_post_fixed_fee_without_the_field_price(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {
        'start': '06:00:00',
        'end': '22:00:00'
    }

    rv = client.post('/v1/bill/fee/fixed/', data=data, headers=headers)
    assert rv.status_code == 400


def test_get_fixed_fee_is_deleted(client):
    fee = FixedFeeFactory()
    client.delete(f'/v1/bill/fee/fixed/{fee.id}/')

    rv = client.get(f'/v1/bill/fee/fixed/{fee.id}/')

    assert rv.status_code == 404
