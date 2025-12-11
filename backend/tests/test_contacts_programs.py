from fastapi.testclient import TestClient
from backend.main import app


client = TestClient(app)


def test_contacts_crud():
    # create
    r = client.post('/contacts', json={'name': 'C1', 'email': 'c1@example.com'})
    assert r.status_code == 201
    c = r.json()
    cid = c['id']

    # list
    l = client.get('/contacts')
    assert l.status_code == 200
    assert any(x['id'] == cid for x in l.json())

    # update
    u = client.put(f'/contacts/{cid}', json={'name': 'C1b', 'email': 'c1b@example.com'})
    assert u.status_code == 200
    assert u.json()['name'] == 'C1b'

    # delete
    d = client.delete(f'/contacts/{cid}')
    assert d.status_code == 204


def test_programs_crud():
    r = client.post('/programs', json={'name': 'P1', 'description': 'd'})
    assert r.status_code == 201
    p = r.json()
    pid = p['id']

    l = client.get('/programs')
    assert l.status_code == 200
    assert any(x['id'] == pid for x in l.json())

    u = client.put(f'/programs/{pid}', json={'name': 'P1b', 'description': 'd2'})
    assert u.status_code == 200
    assert u.json()['name'] == 'P1b'

    d = client.delete(f'/programs/{pid}')
    assert d.status_code == 204
