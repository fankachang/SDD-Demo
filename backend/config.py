import os
import logging
from typing import Dict, Iterable


class Config:
    """Centralized config reader (simple, dependency-free).

    Use `Config()` to access runtime configuration values.
    """

    def __init__(self):
        self.SMTP_HOST = os.getenv("SMTP_HOST")
        self.SMTP_PORT = int(os.getenv("SMTP_PORT", "0") or 0)
        self.SMTP_USER = os.getenv("SMTP_USER")
        self.SMTP_PASS = os.getenv("SMTP_PASS")
        self.SMTP_FROM = os.getenv("SMTP_FROM", "noreply@example.com")
        self.SMTP_USE_TLS = os.getenv("SMTP_USE_TLS", "true").lower() == "true"
        self.SMTP_TIMEOUT = int(os.getenv("SMTP_TIMEOUT", "30"))
        self.DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./dev.db")
        self.SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
        self.SESSION_EXPIRE_MINUTES = int(os.getenv("SESSION_EXPIRE_MINUTES", "60"))
        self.APP_NAME = os.getenv("APP_NAME", "Release Announcements")
        self.APP_ENV = os.getenv("APP_ENV", "development")
        self.DEBUG = os.getenv("DEBUG", "false").lower() == "true"
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    def as_dict(self) -> Dict[str, str]:
        return {
            "SMTP_HOST": self.SMTP_HOST,
            "SMTP_PORT": str(self.SMTP_PORT),
            "SMTP_USER": self.SMTP_USER,
            "SMTP_PASS": self.SMTP_PASS,
            "SMTP_FROM": self.SMTP_FROM,
            "SMTP_USE_TLS": str(self.SMTP_USE_TLS),
            "SMTP_TIMEOUT": str(self.SMTP_TIMEOUT),
            "DATABASE_URL": self.DATABASE_URL,
            "SECRET_KEY": self.SECRET_KEY,
            "SESSION_EXPIRE_MINUTES": str(self.SESSION_EXPIRE_MINUTES),
            "APP_NAME": self.APP_NAME,
            "APP_ENV": self.APP_ENV,
            "DEBUG": str(self.DEBUG),
            "LOG_LEVEL": self.LOG_LEVEL,
        }


def _mask_value(v: str) -> str:
    if not v:
        return v
    # show only last 4 chars if long enough
    if len(v) <= 4:
        return "****"
    return "****" + v[-4:]


SENSITIVE_KEYS = {"SMTP_PASS", "SMTP_USER", "DATABASE_URL", "SECRET_KEY"}


def redact_mapping(
    m: Dict[str, str], sensitive_keys: Iterable[str] = SENSITIVE_KEYS
) -> Dict[str, str]:
    out = {}
    for k, v in (m or {}).items():
        if k in sensitive_keys and v:
            out[k] = _mask_value(v)
        else:
            out[k] = v
    return out


class SecretFilter(logging.Filter):
    """Logging filter that redacts configured sensitive values in log records.

    Attach to loggers via `logger.addFilter(SecretFilter(config))`.
    """

    def __init__(self, cfg: Config):
        super().__init__()
        self._secrets = set()
        for v in cfg.as_dict().values():
            if v:
                self._secrets.add(str(v))

    def _redact(self, text: str) -> str:
        if not text:
            return text
        out = text
        for s in self._secrets:
            if s and s in out:
                out = out.replace(s, _mask_value(s))
        return out

    def filter(self, record: logging.LogRecord) -> bool:  # return True to allow record
        try:
            # Safest approach: compute the formatted message, redact it, and replace
            # the record's msg with the already-formatted, redacted string so
            # handlers/formatters won't re-insert secrets.
            try:
                formatted = record.getMessage()
            except Exception:
                formatted = str(record.msg)

            redacted = self._redact(formatted)
            # replace msg with redacted, and clear args to avoid re-formatting
            record.msg = redacted
            record.args = ()
        except Exception:
            # never raise from a logging filter
            pass
        return True


# module-level default config
cfg = Config()


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    # attach filter once
    if not any(isinstance(f, SecretFilter) for f in logger.filters):
        # build a fresh Config snapshot so tests that set env vars at runtime
        # get the current secret values for redaction
        logger.addFilter(SecretFilter(Config()))
    return logger
