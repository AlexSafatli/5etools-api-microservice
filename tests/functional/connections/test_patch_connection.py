from http import HTTPStatus

from tests.factories import PersonFactory, ConnectionFactory


def test_can_change_connection_connection_type(db, testapp):
    person_from = PersonFactory(first_name='Jim')
    person_to = PersonFactory(first_name='Dwight')
    connection = ConnectionFactory(to_person=person_to, from_person=person_from,
                                   connection_type='friend')
    db.session.commit()
    payload = {
        'connection_type': 'coworker',
    }
    res = testapp.patch('/connections/%d' % connection.id, json=payload)

    assert res.status_code == HTTPStatus.OK

    assert 'id' in res.json
    assert res.json['from_person_id'] == connection.from_person_id
    assert res.json['to_person_id'] == connection.to_person_id
    assert res.json['connection_type'] == 'coworker'  # should no longer be 'friend'

    res = testapp.patch('/connections/%d' % connection.id, json={
        'connection_type': 'foo'
    })  # invalid connection_type

    assert res.status_code != HTTPStatus.OK
