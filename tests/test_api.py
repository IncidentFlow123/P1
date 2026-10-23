from fastapi.testclient import TestClient

from app.main import app, store

client = TestClient(app)

def setup_function():
    store.clear()

def test_health():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'ok'

def test_create_and_resolve_incident():
    created = client.post(
        '/incidents',
        json={'title': 'API inaccessible', 'severity': 'high'},
    )
    assert created.status_code == 201
    incident_id = created.json()['id']
    assert created.json()['status'] == 'open'
    assert len(client.get('/incidents').json()) == 1
    resolved = client.patch(f'/incidents/{incident_id}/resolve')
    assert resolved.status_code == 200
    assert resolved.json()['status'] == 'resolved'

def test_invalid_incident():
    response = client.post('/incidents', json={'title': 'x', 'severity': 'urgent'})
    assert response.status_code == 422

def test_missing_incident():
    assert client.patch('/incidents/99999/resolve').status_code == 404
