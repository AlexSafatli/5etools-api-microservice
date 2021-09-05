from http import HTTPStatus

from tests.factories import ConnectionFactory
from tests.functional.people.test_get_people import EXPECTED_FIELDS as EXPECTED_PEOPLE_FIELDS

EXPECTED_FIELDS = [
    'from_person_id',
    'to_person_id',
    'connection_type',
    'from_person',
    'to_person'
]


def test_can_get_connections(db, testapp):
    ConnectionFactory.create_batch(10)
    db.session.commit()

    res = testapp.get('/connections')

    assert res.status_code == HTTPStatus.OK

    assert len(res.json) == 10
    for connection in res.json:
        for field in EXPECTED_FIELDS:
            assert field in connection
            if field == 'from_person' or field == 'to_person':
                for person_field in EXPECTED_PEOPLE_FIELDS:
                    assert person_field in connection[field]
