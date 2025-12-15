import io
import logging

from backend import config


def test_redact_mapping_masks_sensitive_values(monkeypatch):
    monkeypatch.setenv("SMTP_USER", "user@example.com")
    monkeypatch.setenv("SMTP_PASS", "supersecretpw")
    monkeypatch.setenv("DATABASE_URL", "postgres://u:p@localhost/db")

    cfg = config.Config()
    d = cfg.as_dict()
    redacted = config.redact_mapping(d)

    # Sensitive keys should be masked and original values must not appear
    assert "supersecretpw" not in redacted["SMTP_PASS"]
    assert redacted["SMTP_PASS"].startswith("****")
    assert "postgres://u:p@localhost/db" not in redacted["DATABASE_URL"]
    assert redacted["DATABASE_URL"].startswith("****")


def test_secret_filter_redacts_log_output(monkeypatch):
    monkeypatch.setenv("SMTP_PASS", "topsecret1234")
    cfg = config.Config()

    logger = config.get_logger("test_config_logger")
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    # Log a message that includes the raw secret value as an argument
    logger.info("Sending with password: %s", cfg.SMTP_PASS)
    handler.flush()
    out = stream.getvalue()

    # Raw secret must not appear, masked form should appear
    assert "topsecret1234" not in out
    assert "****" in out
