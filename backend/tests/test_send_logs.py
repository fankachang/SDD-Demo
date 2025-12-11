from fastapi.testclient import TestClient
from backend.main import app
import backend.emailer as emailer


client = TestClient(app)


def test_send_logs_filter_by_program(monkeypatch):
    # create program
    resp = client.post("/programs", json={"name": "FilterP", "description": "d"})
    assert resp.status_code == 201
    program = resp.json()

    # create release
    payload = {
        "program_id": program["id"],
        "version": "0.1.0",
        "notes": "Notes",
        "recipients": [{"email": "x@example.com", "type": "to"}],
    }
    r = client.post("/releases", json=payload)
    assert r.status_code == 201
    release_id = r.json()["id"]

    # simulate smtp success
    def fake_send(subject, body, recipients):
        return [{"email": recipients[0]["email"], "result": "success", "detail": "sent"}]

    monkeypatch.setattr(emailer, "send_synchronously", fake_send)

    s = client.post(f"/releases/{release_id}/send", json={"recipients": payload["recipients"]})
    assert s.status_code == 200

    # query send_logs filtered by program_id
    q = client.get(f"/send_logs?program_id={program['id']}&result=success&page=1&page_size=10")
    assert q.status_code == 200
    data = q.json()
    assert isinstance(data, list)
    assert any(d["release_id"] == release_id for d in data)
