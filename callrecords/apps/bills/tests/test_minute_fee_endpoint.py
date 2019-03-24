import pytest
from tests.factories import MinuteFeeFactory

pytestmark = pytest.mark.django_db(transaction=True)


def test_post_minute_fee(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {
        'price': 0.36,
        'start': '06:00:00',
        'end': '22:00:00'
    }

    rv = client.post('/v1/bill/fee/minute/', data=data, headers=headers)
    assert rv.data is not None


def test_get_minute_fee(client):
    fee = MinuteFeeFactory()

    rv = client.get(f'/v1/bill/fee/minute/{fee.id}/')
    assert rv.status_code == 200


def test_delete_minute_fee(client):
    fee = MinuteFeeFactory()
    rv = client.delete(f'/v1/bill/fee/minute/{fee.id}/')

    assert rv.status_code == 204


def test_fail_put_minute_fee(client):
    fee = MinuteFeeFactory()

    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {
        'price': 0.36
    }

    rv = client.put(f'/v1/bill/fee/minute/{fee.id}/', data=data, headers=headers)
    assert rv.status_code == 405


def test_post_minute_fee_without_the_fields_start_and_end(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {
        'price': 0.36
    }

    rv = client.post('/v1/bill/fee/minute/', data=data, headers=headers)
    assert rv.status_code == 400


def test_post_minute_fee_without_the_field_price(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {
        'start': '06:00:00',
        'end': '22:00:00'
    }

    rv = client.post('/v1/bill/fee/minute/', data=data, headers=headers)
    assert rv.status_code == 400


def test_get_minute_fee_is_deleted(client):
    fee = MinuteFeeFactory()
    client.delete(f'/v1/bill/fee/minute/{fee.id}/')

    rv = client.get(f'/v1/bill/fee/minute/{fee.id}/')

    assert rv.status_code == 404
