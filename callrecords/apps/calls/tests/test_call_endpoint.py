import pytest
from tests.factories import CallStartFactory, FixedFeeFactory


def test_get_call_fail(client):
    rv = client.get('/v1/call/')
    assert rv.status_code == 405
    assert rv.json() is not None


@pytest.mark.django_db(transaction=True)
def test_post_call_start(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {
        "id": 1,
        "source": 10999995555,
        "destination": 10955559999,
        "timestamp": "2017-12-12T15:07:58Z",
        "type": "start",
    }
    rv = client.post('/v1/call/', data=data, headers=headers)
    assert rv.status_code == 201
    assert rv.json() is not None


@pytest.mark.django_db(transaction=True)
def test_post_call_end(client):
    call_start = CallStartFactory()
    FixedFeeFactory()
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {
        'id': call_start.id,
        'timestamp': '2017-12-12T15:07:58Z',
        'type': 'end'
    }
    rv = client.post('/v1/call/', data=data, headers=headers)
    assert rv.status_code == 201
    assert rv.json() is not None


def test_delete_call(client):
    rv = client.delete('/v1/call/1/')

    assert rv.status_code == 404


@pytest.mark.django_db(transaction=True)
def test_post_call_start_without_finalize_last_call_record(client):
    call_start = CallStartFactory()

    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {
        'id': call_start.id + 1,
        'timestamp': '2017-12-12T15:07:58Z',
        'source': call_start.source,
        'destination': 45656587474,
        'type': 'start'
    }

    rv = client.post('/v1/call/', data=data, headers=headers)

    assert rv.status_code == 400
    assert rv.json() is not None


@pytest.mark.django_db(transaction=True)
def test_post_call_start_with_existing_call_id_in_model_call_start(client):
    call_start = CallStartFactory()

    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {
        'id': call_start.id,
        'timestamp': '2017-12-12T15:07:58Z',
        'source': 78999994545,
        'destination': 45656587474,
        'type': 'start'
    }

    rv = client.post('/v1/call/', data=data, headers=headers)
    assert rv.status_code == 400
    assert rv.json() is not None
    assert rv.json() == {'id': ['call start with this id already exists.']}


@pytest.mark.django_db(transaction=True)
def test_post_call_end_without_existing_call_id_in_model_call_start(client):
    call_start = CallStartFactory()

    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {
        'id': call_start.id + 1,
        'timestamp': '2017-12-12T15:07:58Z',
        'type': 'end'
    }

    rv = client.post('/v1/call/', data=data, headers=headers)

    assert rv.status_code == 400
    assert rv.json() is not None
    assert rv.json() == [f'No exist the call id {call_start.id + 1} in start call records']


@pytest.mark.django_db(transaction=True)
def test_post_call_start_without_data(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    rv = client.post('/v1/call/', headers=headers)

    assert rv.status_code == 400
    assert rv.json() is not None
