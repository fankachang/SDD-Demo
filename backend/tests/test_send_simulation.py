from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_partial_failure_creates_sendlog(smtp_stub):
    smtp_stub.set_behavior("partial")

    # create program
    resp = client.post("/programs", json={"name": "SimP", "description": "d"})
    assert resp.status_code == 201
    program = resp.json()

    # create release
    payload = {
        "program_id": program["id"],
        "version": "0.2.0",
        "notes": "Notes",
        "recipients": [
            {"email": "a@example.com", "type": "to"},
            {"email": "b@example.com", "type": "to"},
        ],
    }
    r = client.post("/releases", json=payload)
    assert r.status_code == 201
    rid = r.json()["id"]

    s = client.post(f"/releases/{rid}/send", json={"recipients": payload["recipients"]})
    assert s.status_code == 200
    data = s.json()
    assert data["results"] and any(r["result"] == "failure" for r in data["results"])

    # ensure send_log recorded with failure
    logs = client.get(f"/send_logs?program_id={program['id']}")
    assert logs.status_code == 200
    found = any(l["release_id"] == rid and l["result"] == "failure" for l in logs.json())
    assert found


def test_exception_records_sendlog(smtp_stub):
    smtp_stub.set_behavior("failure")

    resp = client.post("/programs", json={"name": "SimP2", "description": "d2"})
    program = resp.json()
    payload = {
        "program_id": program["id"],
        "version": "9.9.9",
        "notes": "Notes",
        "recipients": [{"email": "x@example.com", "type": "to"}],
    }
    r = client.post("/releases", json=payload)
    rid = r.json()["id"]

    s = client.post(f"/releases/{rid}/send", json={"recipients": payload["recipients"]})
    assert s.status_code == 200
    data = s.json()
    # results should indicate internal failure
    assert data["results"] and data["results"][0]["result"] == "failure"

    logs = client.get(f"/send_logs?program_id={program['id']}")
    assert logs.status_code == 200
    entries = logs.json()
    assert any(e["release_id"] == rid and e["result"] == "failure" and "simulated connection failure" in (e.get("detail") or "") for e in entries)
