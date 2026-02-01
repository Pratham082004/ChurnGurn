from datetime import datetime
from app.extensions import db
from app.models.base import UUIDMixin

class UsageLog(UUIDMixin, db.Model):
    __tablename__ = "usage_logs"

    company_id = db.Column(
        db.UUID(as_uuid=True),
        db.ForeignKey("companies.id"),
        nullable=False
    )

    usage_type = db.Column(db.String(30))  # PREDICTION / API / ALERT
    count = db.Column(db.Integer, default=1)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
