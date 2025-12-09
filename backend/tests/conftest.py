import pytest


class SMTPStub:
    def __init__(self, monkeypatch):
        self.behavior = "success"
        self.calls = []
        self._monkeypatch = monkeypatch
        monkeypatch.setattr("backend.emailer.send_synchronously", self._impl)

    def _impl(self, subject, body, recipients, timeout=30):
        self.calls.append({"subject": subject, "recipients": recipients})
        if self.behavior == "success":
            return [{"email": r["email"], "result": "success", "detail": "sent"} for r in recipients]
        if self.behavior == "partial":
            out = []
            for i, r in enumerate(recipients):
                if i % 2 == 0:
                    out.append({"email": r["email"], "result": "success", "detail": "sent"})
                else:
                    out.append({"email": r["email"], "result": "failure", "detail": "simulated error"})
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
