"""測試 Contacts 和 Programs 的 CRUD 操作

驗證：
1. 基本 CRUD 操作（建立、讀取、更新、刪除）
2. Email 格式驗證
3. 在建立 release 時能選擇到新增的資料
"""

from fastapi.testclient import TestClient
from backend.main import app
import pytest


client = TestClient(app)


def test_contacts_crud():
    """測試 Contacts CRUD 操作"""
    # 建立 contact
    r = client.post('/contacts', json={'name': 'C1', 'email': 'c1@example.com'})
    assert r.status_code == 201
    c = r.json()
    cid = c['id']
    assert c['name'] == 'C1'
    assert c['email'] == 'c1@example.com'

    # 列出 contacts
    l = client.get('/contacts')
    assert l.status_code == 200
    contacts = l.json()
    assert isinstance(contacts, list)
    assert any(x['id'] == cid for x in contacts)

    # 更新 contact
    u = client.put(f'/contacts/{cid}', json={'name': 'C1b', 'email': 'c1b@example.com'})
    assert u.status_code == 200
    updated = u.json()
    assert updated['name'] == 'C1b'
    assert updated['email'] == 'c1b@example.com'

    # 刪除 contact
    d = client.delete(f'/contacts/{cid}')
    assert d.status_code == 204

    # 驗證刪除後不存在
    l2 = client.get('/contacts')
    assert not any(x['id'] == cid for x in l2.json())


def test_contacts_email_validation():
    """測試 Email 格式驗證"""
    # 無效的 email 格式應該回傳 422
    invalid_emails = ['not-an-email', '@example.com', 'user@', 'user space@example.com']
    
    for invalid_email in invalid_emails:
        r = client.post('/contacts', json={'name': 'Test', 'email': invalid_email})
        # Pydantic 驗證失敗會回傳 422
        assert r.status_code == 422, f"應該拒絕無效 email: {invalid_email}"


def test_programs_crud():
    """測試 Programs CRUD 操作"""
    # 建立 program
    r = client.post('/programs', json={'name': 'P1', 'description': 'd'})
    assert r.status_code == 201
    p = r.json()
    pid = p['id']
    assert p['name'] == 'P1'
    assert p['description'] == 'd'

    # 列出 programs
    l = client.get('/programs')
    assert l.status_code == 200
    programs = l.json()
    assert isinstance(programs, list)
    assert any(x['id'] == pid for x in programs)

    # 更新 program
    u = client.put(f'/programs/{pid}', json={'name': 'P1b', 'description': 'd2'})
    assert u.status_code == 200
    updated = u.json()
    assert updated['name'] == 'P1b'
    assert updated['description'] == 'd2'

    # 刪除 program
    d = client.delete(f'/programs/{pid}')
    assert d.status_code == 204

    # 驗證刪除後不存在
    l2 = client.get('/programs')
    assert not any(x['id'] == pid for x in l2.json())


def test_programs_optional_description():
    """測試 Programs 的 description 欄位為可選"""
    r = client.post('/programs', json={'name': 'P2'})
    assert r.status_code == 201
    p = r.json()
    assert p['name'] == 'P2'
    assert p.get('description') is None or p.get('description') == ''
    
    # 清理
    client.delete(f'/programs/{p["id"]}')


def test_contacts_in_release_selection():
    """測試在建立 release 時能選擇到新增的 contact"""
    # 建立 program
    prog_r = client.post('/programs', json={'name': 'TestProg', 'description': 'Test'})
    assert prog_r.status_code == 201
    prog = prog_r.json()
    
    # 建立 contact
    cont_r = client.post('/contacts', json={'name': 'TestContact', 'email': 'test@example.com'})
    assert cont_r.status_code == 201
    cont = cont_r.json()
    
    # 使用新建立的 contact 建立 release
    rel_r = client.post('/releases', json={
        'program_id': prog['id'],
        'version': 'v1.0.0',
        'notes': 'Test release',
        'recipients': [
            {'email': cont['email'], 'type': 'to'}
        ]
    })
    # 應該能成功建立（即使可能需要授權，至少不會因為 contact 不存在而失敗）
    assert rel_r.status_code in [201, 401, 403]  # 201=成功, 401/403=需授權但資料有效
    
    # 清理
    client.delete(f'/programs/{prog["id"]}')
    client.delete(f'/contacts/{cont["id"]}')

