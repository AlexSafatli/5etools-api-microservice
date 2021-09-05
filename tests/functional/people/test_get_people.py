from http import HTTPStatus

from tests.factories import PersonFactory, ConnectionFactory

EXPECTED_FIELDS = [
    'id',
    'first_name',
    'last_name',
    'email',
]

NUMBER_MUTUAL_FRIENDS = 5


def test_can_get_people(db, testapp):
    PersonFactory.create_batch(10)
    db.session.commit()

    res = testapp.get('/people')

    assert res.status_code == HTTPStatus.OK

    assert len(res.json) == 10
    for person in res.json:
        for field in EXPECTED_FIELDS:
            assert field in person


def test_can_get_people_mutual_friends(db, testapp):
    person = PersonFactory()
    target = PersonFactory()

    # some decoy connections (not mutual)
    ConnectionFactory.create_batch(2, to_person=person)
    ConnectionFactory.create_batch(2, to_person=target)

    # actual mutual friends
    mutual_friends = PersonFactory.create_batch(NUMBER_MUTUAL_FRIENDS)
    for f in mutual_friends:
        ConnectionFactory(from_person=person, to_person=f, connection_type='friend')
        ConnectionFactory(from_person=target, to_person=f, connection_type='friend')

    # mutual connections, but not friends
    decoy1 = PersonFactory()
    decoy2 = PersonFactory()
    ConnectionFactory(from_person=person, to_person=decoy1, connection_type='coworker')
    ConnectionFactory(from_person=target, to_person=decoy2, connection_type='coworker')

    db.session.commit()

    expected_mutual_friend_ids = [f.id for f in mutual_friends]
    received_mutual_friend_ids = []
    swapped_mutual_friend_ids = []

    # check normal case
    res = testapp.get('/people/%d/mutual_friends?target_id=%d' % (person.id, target.id))

    assert res.status_code == HTTPStatus.OK

    assert len(res.json) == NUMBER_MUTUAL_FRIENDS
    for person_obj in res.json:
        for field in EXPECTED_FIELDS:
            assert field in person_obj
        person_id = person_obj['id']
        assert person_id in expected_mutual_friend_ids
        received_mutual_friend_ids.append(person_id)

    assert len(set(expected_mutual_friend_ids).intersection(
        set(received_mutual_friend_ids))) == NUMBER_MUTUAL_FRIENDS  # correct IDs, no dupes

    # check if same swapping the IDs
    res = testapp.get('/people/%d/mutual_friends?target_id=%d' % (target.id, person.id))

    assert res.status_code == HTTPStatus.OK

    assert len(res.json) == NUMBER_MUTUAL_FRIENDS
    for person_obj in res.json:
        swapped_mutual_friend_ids.append(person_obj['id'])
    assert received_mutual_friend_ids == swapped_mutual_friend_ids
