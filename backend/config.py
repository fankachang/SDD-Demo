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
        self.SMTP_TIMEOUT = int(os.getenv("SMTP_TIMEOUT", "30"))
        self.DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./dev.db")

    def as_dict(self) -> Dict[str, str]:
        return {
            "SMTP_HOST": self.SMTP_HOST,
            "SMTP_PORT": str(self.SMTP_PORT),
            "SMTP_USER": self.SMTP_USER,
            "SMTP_PASS": self.SMTP_PASS,
            "SMTP_TIMEOUT": str(self.SMTP_TIMEOUT),
            "DATABASE_URL": self.DATABASE_URL,
        }


def _mask_value(v: str) -> str:
    if not v:
        return v
    # show only last 4 chars if long enough
    if len(v) <= 4:
        return "****"
    return "****" + v[-4:]


SENSITIVE_KEYS = {"SMTP_PASS", "SMTP_USER", "DATABASE_URL"}


def redact_mapping(m: Dict[str, str], sensitive_keys: Iterable[str] = SENSITIVE_KEYS) -> Dict[str, str]:
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
            if isinstance(record.msg, str):
                record.msg = self._redact(record.msg)
            if record.args:
                if isinstance(record.args, (list, tuple)):
                    record.args = tuple(self._redact(str(a)) for a in record.args)
                elif isinstance(record.args, dict):
                    record.args = {k: self._redact(str(v)) for k, v in record.args.items()}
                else:
                    record.args = self._redact(str(record.args))
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
        logger.addFilter(SecretFilter(cfg))
    return logger
