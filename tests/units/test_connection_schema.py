from datetime import date

import pytest
from marshmallow import ValidationError
from tests.factories import PersonFactory

from connections.schemas import ConnectionSchema


@pytest.mark.xfail
@pytest.mark.parametrize('from_dob, to_dob, conn_type, error_message', [
    pytest.param((1950, 10, 1), (1990, 10, 1), 'son', 'son older than parent'),
    pytest.param((1990, 10, 1), (1950, 10, 1), 'father', 'father younger than child'),
    pytest.param((1950, 10, 1), (1990, 10, 1), 'daughter', 'daughter older than parent'),
    pytest.param((1990, 10, 1), (1950, 10, 1), 'mother', 'mother younger than child'),
])
def test_schema_validates_parent_older_than_child(db, from_dob, to_dob, conn_type, error_message):
    from_person = PersonFactory(date_of_birth=date(*from_dob))
    to_person = PersonFactory(date_of_birth=date(*to_dob))
    db.session.commit()

    schema = ConnectionSchema()
    with pytest.raises(ValidationError) as exception_info:
        schema.load({'from_person_id': from_person.id, 'to_person_id': to_person.id,
                    'connection_type': conn_type})
    schema_validation_messages = exception_info.value.messages['_schema']
    assert len(schema_validation_messages) == 1
    assert schema_validation_messages[0] == f'Invalid connection - {error_message}.'
