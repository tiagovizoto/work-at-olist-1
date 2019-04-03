import pytest
from datetime import datetime
from tests.factories import BillFactory, MinuteFeeFactory, FixedFeeFactory

pytestmark = pytest.mark.django_db(transaction=True)


def test_fail_post_bill(client):
    bill = BillFactory()
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {
        'fixed_fee': bill.fixed_fee.id,
        'price': bill.price,
        'start_call': bill.call_start,
        'end_call': bill.call_end,
    }
    rv = client.post('/v1/bill/4197020434/', data=data, headers=headers)
    assert rv.status_code == 405


def test_fail_delete_bill(client):
    rv = client.delete('/v1/bill/4197020434/')
    assert rv.status_code == 405


def test_fail_put_bill(client):
    rv = client.delete('/v1/bill/4197020434/')
    assert rv.status_code == 405


def test_get_last_bill(client):
    MinuteFeeFactory()
    FixedFeeFactory()
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data_s = {
        'id': 1,
        'source': 10999995555,
        'destination': 10955559999,
        'timestamp': f'{datetime.today().year}-{datetime.today().month - 1}-05T15:07:58Z',
        'type': 'start',
    }

    data_e = {
        'id': 1,
        'timestamp': f'{datetime.today().year}-{datetime.today().month - 1}-12T17:07:58Z',
        'type': 'end'
    }
    client.post('/v1/call/', data=data_s, headers=headers)
    client.post('/v1/call/', data=data_e, headers=headers)
    rv = client.get("/v1/bill/10999995555/")
    assert rv.status_code == 200


def test_get_year_bill(client):
    MinuteFeeFactory()
    FixedFeeFactory()
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data_s = {
        'id': 1,
        'source': 10999995555,
        'destination': 10955559999,
        'timestamp': '2017-12-12T15:07:58Z',
        'type': 'start',
    }

    data_e = {
        'id': 1,
        'timestamp': '2017-12-12T17:07:58Z',
        'type': 'end'
    }
    client.post('/v1/call/', data=data_s, headers=headers)
    client.post('/v1/call/', data=data_e, headers=headers)
    rv = client.get("/v1/bill/10999995555/2017/")
    assert rv.status_code == 200
    assert rv.json is not None


def test_get_year_month_bill(client):
    MinuteFeeFactory()
    FixedFeeFactory()
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data_s = {
        'id': 1,
        'source': 10999995555,
        'destination': 10955559999,
        'timestamp': '2017-12-12T15:07:58Z',
        'type': 'start',
    }

    data_e = {
        'id': 1,
        'timestamp': '2017-12-12T17:07:58Z',
        'type': 'end'
    }
    client.post('/v1/call/', data=data_s, headers=headers)
    client.post('/v1/call/', data=data_e, headers=headers)
    rv = client.get("/v1/bill/10999995555/2017/12/")
    assert rv.status_code == 200
    assert rv.json is not None


def test_fail_get_year_future_bill(client):
    MinuteFeeFactory()
    FixedFeeFactory()
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data_s = {
        'id': 1,
        'source': 10999995555,
        'destination': 10955559999,
        'timestamp': '2017-12-12T15:07:58Z',
        'type': 'start',
    }

    data_e = {
        'id': 1,
        'timestamp': '2017-12-12T17:07:58Z',
        'type': 'end'
    }
    client.post('/v1/call/', data=data_s, headers=headers)
    client.post('/v1/call/', data=data_e, headers=headers)
    rv = client.get("/v1/bill/10999995555/2020/")
    assert rv.status_code == 400
    assert rv.json is not None


def test_fail_get_year_month_future_bill(client):
    MinuteFeeFactory()
    FixedFeeFactory()
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data_s = {
        'id': 1,
        'source': 10999995555,
        'destination': 10955559999,
        'timestamp': '2017-12-12T15:07:58Z',
        'type': 'start',
    }

    data_e = {
        'id': 1,
        'timestamp': '2017-12-17T15:07:58Z',
        'type': 'end'
    }
    client.post('/v1/call/', data=data_s, headers=headers)
    client.post('/v1/call/', data=data_e, headers=headers)
    rv = client.get("/v1/bill/10999995555/2120/05/")
    assert rv.status_code == 400
    assert rv.json is not None
