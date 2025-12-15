from typing import Dict, Any
from sqlalchemy.orm import Session
from .. import models


def create_release(db: Session, payload: Dict[str, Any]):
    release = models.Release(
        program_id=payload["program_id"],
        version=payload["version"],
        notes=payload.get("notes"),
    )
    db.add(release)
    db.commit()
    db.refresh(release)

    for r in payload.get("recipients", []):
        rr = models.ReleaseRecipient(
            release_id=release.id, email=r["email"], recipient_type=r.get("type", "to")
        )
        db.add(rr)
    db.commit()
    return release


def render_release_preview(db: Session, release_id: int, render_fn):
    release = db.query(models.Release).filter(models.Release.id == release_id).first()
    if not release:
        return None
    subject = f"Release {release.version}"
    body_template = "<h1>{{ subject }}</h1><p>{{ notes }}</p>"
    context = {"subject": subject, "notes": release.notes or ""}
    return render_fn(subject, body_template, context)
