from typing import List, Dict, Any
from sqlalchemy.orm import Session
from .. import models, emailer
from ..config import get_logger

logger = get_logger(__name__)


def send_release_synchronously(db: Session, release_id: int, recipients: List[Dict[str, Any]]):
    """Send a release synchronously using backend.emailer and record a SendLog.

    Returns: dict with keys: send_log_id, results
    """
    # fetch release for subject/body
    release = db.query(models.Release).filter(models.Release.id == release_id).first()
    if not release:
        raise ValueError("Release not found")

    subject = f"Release {release.version}"
    body_template = "{{ notes }}"
    context = {"notes": release.notes or ""}
    rendered = emailer.render_template(subject, body_template, context)

    try:
        logger.info("Sending release %s to %d recipients", release.id, len(recipients))
        results = emailer.send_synchronously(rendered["subject"], rendered["body"], recipients)

        overall_result = "success"
        details = []
        for r in results:
            details.append(f"{r['email']}:{r['result']}")
            if r["result"] != "success":
                overall_result = "failure"

        log = models.SendLog(release_id=release.id, result=overall_result, detail=";".join(details))
        db.add(log)
        if overall_result == "success":
            release.status = models.ReleaseStatus.sent
        db.commit()
        db.refresh(log)

        return {"send_log_id": log.id, "results": results}
    except Exception as e:
        # record failure in SendLog for auditing
        msg = str(e)
        logger.exception("Exception while sending release %s: %s", release.id, msg)
        log = models.SendLog(release_id=release.id, result="failure", detail=msg)
        db.add(log)
        db.commit()
        db.refresh(log)
        return {"send_log_id": log.id, "results": [{"email": "<internal>", "result": "failure", "detail": msg}]}
