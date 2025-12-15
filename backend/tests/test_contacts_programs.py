"""測試 Contacts 和 Programs 的 CRUD 操作

驗證：
1. 基本 CRUD 操作（建立、讀取、更新、刪除）
2. Email 格式驗證
3. 在建立 release 時能選擇到新增的資料
"""


def test_contacts_crud(client, auth_headers):
    """測試 Contacts CRUD 操作"""
    # 建立 contact
    r = client.post(
        "/contacts",
        json={"name": "C1", "email": "c1@example.com"},
        headers=auth_headers,
    )
    assert r.status_code == 201
    c = r.json()
    cid = c["id"]
    assert c["name"] == "C1"
    assert c["email"] == "c1@example.com"

    # 列出 contacts
    resp = client.get("/contacts", headers=auth_headers)
    assert resp.status_code == 200
    contacts = resp.json()
    assert isinstance(contacts, list)
    assert any(x["id"] == cid for x in contacts)

    # 更新 contact
    u = client.put(
        f"/contacts/{cid}",
        json={"name": "C1b", "email": "c1b@example.com"},
        headers=auth_headers,
    )
    assert u.status_code == 200
    updated = u.json()
    assert updated["name"] == "C1b"
    assert updated["email"] == "c1b@example.com"

    # 刪除 contact
    d = client.delete(f"/contacts/{cid}", headers=auth_headers)
    assert d.status_code == 204

    # 驗證刪除後不存在
    l2 = client.get("/contacts", headers=auth_headers)
    assert not any(x["id"] == cid for x in l2.json())


def test_contacts_email_validation(client, auth_headers):
    """測試 Email 格式驗證"""
    # 無效的 email 格式應該回傳 422
    invalid_emails = ["not-an-email", "@example.com", "user@", "user space@example.com"]

    for invalid_email in invalid_emails:
        r = client.post(
            "/contacts",
            json={"name": "Test", "email": invalid_email},
            headers=auth_headers,
        )
        # Pydantic 驗證失敗會回傳 422
        assert r.status_code == 422, f"應該拒絕無效 email: {invalid_email}"


def test_programs_crud(client, auth_headers):
    """測試 Programs CRUD 操作"""
    # 建立 program
    r = client.post(
        "/programs", json={"name": "P1", "description": "d"}, headers=auth_headers
    )
    assert r.status_code == 201
    p = r.json()
    pid = p["id"]
    assert p["name"] == "P1"
    assert p["description"] == "d"

    # 列出 programs
    resp = client.get("/programs", headers=auth_headers)
    assert resp.status_code == 200
    programs = resp.json()
    assert isinstance(programs, list)
    assert any(x["id"] == pid for x in programs)

    # 更新 program
    u = client.put(
        f"/programs/{pid}",
        json={"name": "P1b", "description": "d2"},
        headers=auth_headers,
    )
    assert u.status_code == 200
    updated = u.json()
    assert updated["name"] == "P1b"
    assert updated["description"] == "d2"

    # 刪除 program
    d = client.delete(f"/programs/{pid}", headers=auth_headers)
    assert d.status_code == 204

    # 驗證刪除後不存在
    l2 = client.get("/programs", headers=auth_headers)
    assert not any(x["id"] == pid for x in l2.json())


def test_programs_optional_description(client, auth_headers):
    """測試 Programs 的 description 欄位為可選"""
    r = client.post("/programs", json={"name": "P2"}, headers=auth_headers)
    assert r.status_code == 201
    p = r.json()
    assert p["name"] == "P2"
    assert p.get("description") is None or p.get("description") == ""

    # 清理
    client.delete(f'/programs/{p["id"]}', headers=auth_headers)


def test_contacts_in_release_selection(client, auth_headers):
    """測試在建立 release 時能選擇到新增的 contact"""
    # 建立 program
    prog_r = client.post(
        "/programs",
        json={"name": "TestProg", "description": "Test"},
        headers=auth_headers,
    )
    assert prog_r.status_code == 201
    prog = prog_r.json()

    # 建立 contact
    cont_r = client.post(
        "/contacts",
        json={"name": "TestContact", "email": "test@example.com"},
        headers=auth_headers,
    )
    assert cont_r.status_code == 201
    cont = cont_r.json()

    # 使用新建立的 contact 建立 release
    rel_r = client.post(
        "/releases",
        json={
            "program_id": prog["id"],
            "version": "v1.0.0",
            "notes": "Test release",
            "recipients": [{"email": cont["email"], "type": "to"}],
        },
        headers=auth_headers,
    )
    # 應該能成功建立
    assert rel_r.status_code == 201

    # 清理
    client.delete(f'/programs/{prog["id"]}', headers=auth_headers)
    client.delete(f'/contacts/{cont["id"]}', headers=auth_headers)
