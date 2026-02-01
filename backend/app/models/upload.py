from datetime import datetime
from app.extensions import db
from app.models.base import UUIDMixin

class Upload(UUIDMixin, db.Model):
    __tablename__ = "uploads"

    company_id = db.Column(
        db.UUID(as_uuid=True),
        db.ForeignKey("companies.id"),
        nullable=False
    )

    filename = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(30), default="PENDING")

    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
