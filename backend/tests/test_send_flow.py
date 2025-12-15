import backend.emailer as emailer


def test_send_success(client, auth_headers, monkeypatch):
    # create program
    resp = client.post(
        "/programs", json={"name": "P", "description": "d"}, headers=auth_headers
    )
    assert resp.status_code == 201
    program = resp.json()

    # create release
    payload = {
        "program_id": program["id"],
        "version": "1.0.1",
        "notes": "Notes",
        "recipients": [{"email": "a@example.com", "type": "to"}],
    }
    r = client.post("/releases", json=payload, headers=auth_headers)
    assert r.status_code == 201
    release_id = r.json()["id"]

    # simulate smtp success by patching send_synchronously
    def fake_send(subject, body, recipients):
        return [
            {"email": recipients[0]["email"], "result": "success", "detail": "sent"}
        ]

    monkeypatch.setattr(emailer, "send_synchronously", fake_send)

    s = client.post(
        f"/releases/{release_id}/send",
        json={"recipients": [{"email": "a@example.com", "type": "to"}]},
        headers=auth_headers,
    )
    assert s.status_code == 200
    data = s.json()
    assert "send_log_id" in data
    assert len(data["results"]) == 1


def test_send_partial_failure(client, auth_headers, monkeypatch):
    resp = client.post(
        "/programs", json={"name": "P2", "description": "d2"}, headers=auth_headers
    )
    assert resp.status_code == 201
    program = resp.json()

    payload = {
        "program_id": program["id"],
        "version": "2.0.0",
        "notes": "Notes",
        "recipients": [
            {"email": "ok@example.com", "type": "to"},
            {"email": "bad@example.com", "type": "to"},
        ],
    }
    r = client.post("/releases", json=payload, headers=auth_headers)
    assert r.status_code == 201
    rid = r.json()["id"]

    def fake_send(subject, body, recipients):
        return [
            {"email": "ok@example.com", "result": "success", "detail": "sent"},
            {"email": "bad@example.com", "result": "failure", "detail": "smtp error"},
        ]

    monkeypatch.setattr(emailer, "send_synchronously", fake_send)

    s = client.post(
        f"/releases/{rid}/send",
        json={"recipients": payload["recipients"]},
        headers=auth_headers,
    )
    assert s.status_code == 200
    data = s.json()
    assert any(r["result"] == "failure" for r in data["results"])
