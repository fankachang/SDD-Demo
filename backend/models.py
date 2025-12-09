from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, ForeignKey, Index
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from .db import Base


class RoleEnum(str, enum.Enum):
    admin = "admin"
    publisher = "publisher"


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)


class Program(Base):
    __tablename__ = "programs"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)


class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, index=True)
    group = Column(String, nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)


class ReleaseStatus(str, enum.Enum):
    draft = "draft"
    previewed = "previewed"
    sent = "sent"


class Release(Base):
    __tablename__ = "releases"
    id = Column(Integer, primary_key=True, index=True)
    program_id = Column(Integer, ForeignKey("programs.id"), nullable=False)
    version = Column(String, nullable=False)
    notes = Column(Text)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    status = Column(Enum(ReleaseStatus), default=ReleaseStatus.draft)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    recipients = relationship("ReleaseRecipient", back_populates="release")


class RecipientType(str, enum.Enum):
    to = "to"
    cc = "cc"
    bcc = "bcc"


class ReleaseRecipient(Base):
    __tablename__ = "release_recipients"
    id = Column(Integer, primary_key=True, index=True)
    release_id = Column(Integer, ForeignKey("releases.id"))
    contact_id = Column(Integer, ForeignKey("contacts.id"), nullable=True)
    email = Column(String, nullable=False)
    recipient_type = Column(Enum(RecipientType), nullable=False)

    release = relationship("Release", back_populates="recipients")


class SendResult(str, enum.Enum):
    success = "success"
    failure = "failure"
    timeout = "timeout"


class SendLog(Base):
    __tablename__ = "send_logs"
    id = Column(Integer, primary_key=True, index=True)
    release_id = Column(Integer, ForeignKey("releases.id"), index=True)
    sent_at = Column(DateTime, default=datetime.utcnow)
    result = Column(Enum(SendResult))
    detail = Column(Text)

    __table_args__ = (
        Index("ix_send_logs_sent_at", "sent_at"),
        Index("ix_send_logs_release_id", "release_id"),
    )
