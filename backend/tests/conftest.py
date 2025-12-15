import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.main import app
from backend.db import Base, get_db
from backend.models import User
from backend.auth import hash_password, create_session


# 測試資料庫設定 - 使用內存資料庫並使用 StaticPool 確保連接一致性
TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="function")
def db_session():
    """建立測試資料庫 session - 每個測試使用獨立的內存資料庫"""
    # 使用 StaticPool 確保所有連接都使用同一個內存資料庫
    test_engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,  # 使用靜態池確保連接一致性
    )
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine,
        expire_on_commit=False,  # 避免在commit後過期對象
    )

    Base.metadata.create_all(bind=test_engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=test_engine)
        test_engine.dispose()


@pytest.fixture(scope="function")
def client(db_session):
    """建立測試客戶端並覆寫資料庫依賴"""

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def test_admin_user(db_session):
    """建立測試用 admin 使用者"""
    admin_user = User(
        email="admin@test.com",
        password_hash=hash_password("admin123"),
        role="admin",
        name="Test Admin",
    )
    db_session.add(admin_user)
    db_session.commit()
    db_session.refresh(admin_user)
    return admin_user


@pytest.fixture(scope="function")
def test_publisher_user(db_session):
    """建立測試用 publisher 使用者"""
    publisher_user = User(
        email="publisher@test.com",
        password_hash=hash_password("pub123"),
        role="publisher",
        name="Test Publisher",
    )
    db_session.add(publisher_user)
    db_session.commit()
    db_session.refresh(publisher_user)
    return publisher_user


@pytest.fixture(scope="function")
def admin_token(test_admin_user):
    """產生 admin 使用者的認證 token"""
    return create_session(
        user_id=test_admin_user.id,
        user_email=test_admin_user.email,
        user_role=test_admin_user.role,
    )


@pytest.fixture(scope="function")
def publisher_token(test_publisher_user):
    """產生 publisher 使用者的認證 token"""
    return create_session(
        user_id=test_publisher_user.id,
        user_email=test_publisher_user.email,
        user_role=test_publisher_user.role,
    )


@pytest.fixture(scope="function")
def auth_headers(admin_token):
    """產生授權標頭（預設使用 admin token）"""
    return {"Authorization": f"Bearer {admin_token}"}


class SMTPStub:
    def __init__(self, monkeypatch):
        self.behavior = "success"
        self.calls = []
        self._monkeypatch = monkeypatch
        monkeypatch.setattr("backend.emailer.send_synchronously", self._impl)

    def _impl(self, subject, body, recipients, timeout=30):
        self.calls.append({"subject": subject, "recipients": recipients})
        if self.behavior == "success":
            return [
                {"email": r["email"], "result": "success", "detail": "sent"}
                for r in recipients
            ]
        if self.behavior == "partial":
            out = []
            for i, r in enumerate(recipients):
                if i % 2 == 0:
                    out.append(
                        {"email": r["email"], "result": "success", "detail": "sent"}
                    )
                else:
                    out.append(
                        {
                            "email": r["email"],
                            "result": "failure",
                            "detail": "simulated error",
                        }
                    )
            return out
        if self.behavior == "failure":
            raise ConnectionError("simulated connection failure")
        if self.behavior == "timeout":
            raise TimeoutError("simulated timeout")
        # default fallback
        return []

    def set_behavior(self, b: str):
        self.behavior = b


@pytest.fixture
def smtp_stub(monkeypatch):
    return SMTPStub(monkeypatch)
