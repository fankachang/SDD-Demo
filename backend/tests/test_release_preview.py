import os
from fastapi.testclient import TestClient
from backend.main import app


client = TestClient(app)


def test_create_and_preview_release():
    # create program
    resp = client.post("/programs", json={"name": "Test Program", "description": "desc"})
    assert resp.status_code == 201
    program = resp.json()

    # create release
    payload = {
        "program_id": program["id"],
        "version": "1.0.0",
        "notes": "Release notes",
        "recipients": [{"email": "alice@example.com", "type": "to"}],
    }
    r = client.post("/releases", json=payload)
    assert r.status_code == 201
    data = r.json()
    release_id = data["id"]

    # preview
    p = client.get(f"/releases/{release_id}/preview")
    assert p.status_code == 200
    assert "Release 1.0.0" in p.text or "Release: 1.0.0" in p.text
