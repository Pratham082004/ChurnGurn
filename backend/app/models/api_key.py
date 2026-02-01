import uuid
from datetime import datetime
from app.extensions import db
from app.models.base import UUIDMixin

class APIKey(UUIDMixin, db.Model):
    __tablename__ = "api_keys"

    company_id = db.Column(
        db.UUID(as_uuid=True),
        db.ForeignKey("companies.id"),
        nullable=False
    )

    key = db.Column(db.String(64), unique=True, default=lambda: uuid.uuid4().hex)
    is_active = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
