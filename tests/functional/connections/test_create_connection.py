from datetime import date
from http import HTTPStatus

import pytest
from tests.factories import PersonFactory

from connections.models.connection import Connection


def test_can_create_connection(db, testapp):
    person_from = PersonFactory(first_name='Jim')
    person_to = PersonFactory(first_name='Dwight')
    db.session.commit()
    payload = {
        'from_person_id': person_from.id,
        'to_person_id': person_to.id,
        'connection_type': 'coworker',
    }
    res = testapp.post('/connections', json=payload)

    assert res.status_code == HTTPStatus.CREATED

    assert 'id' in res.json

    connection = Connection.query.get(res.json['id'])

    assert connection is not None
    assert connection.from_person_id == person_from.id
    assert connection.to_person_id == person_to.id
    assert connection.connection_type.value == 'coworker'


@pytest.mark.xfail
def test_create_connection_parent_and_child_validation(db, testapp):
    parent = PersonFactory(date_of_birth=date(1950, 10, 1))
    child = PersonFactory(date_of_birth=date(1990, 10, 1))
    db.session.commit()
    payload = {
        'from_person_id': parent.id,
        'to_person_id': child.id,
        'connection_type': 'son',
    }
    res = testapp.post('/connections', json=payload)

    assert res.status_code == HTTPStatus.BAD_REQUEST

    assert res.status_code == HTTPStatus.BAD_REQUEST
    assert res.json['description'] == 'Input failed validation.'
    errors = res.json['errors']
    assert len(errors['_schema']) == 1

    assert errors['_schema'][0] == 'Invalid connection - son older than parent.'
