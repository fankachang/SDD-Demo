import backend.emailer as emailer


def test_send_logs_filter_by_program(client, auth_headers, monkeypatch):
    # create program
    resp = client.post(
        "/programs", json={"name": "FilterP", "description": "d"}, headers=auth_headers
    )
    assert resp.status_code == 201
    program = resp.json()

    # create release
    payload = {
        "program_id": program["id"],
        "version": "0.1.0",
        "notes": "Notes",
        "recipients": [{"email": "x@example.com", "type": "to"}],
    }
    r = client.post("/releases", json=payload, headers=auth_headers)
    assert r.status_code == 201
    release_id = r.json()["id"]

    # simulate smtp success
    def fake_send(subject, body, recipients):
        return [
            {"email": recipients[0]["email"], "result": "success", "detail": "sent"}
        ]

    monkeypatch.setattr(emailer, "send_synchronously", fake_send)

    s = client.post(
        f"/releases/{release_id}/send",
        json={"recipients": payload["recipients"]},
        headers=auth_headers,
    )
    assert s.status_code == 200

    # query send_logs filtered by program_id
    q = client.get(
        f"/send_logs?program_id={program['id']}&result=success&page=1&page_size=10",
        headers=auth_headers,
    )
    assert q.status_code == 200
    data = q.json()
    assert isinstance(data, list)
    assert any(d["release_id"] == release_id for d in data)
