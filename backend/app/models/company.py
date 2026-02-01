from datetime import datetime
from app.extensions import db
from app.models.base import UUIDMixin

class Company(UUIDMixin, db.Model):
    __tablename__ = "companies"

    name = db.Column(db.String(120), nullable=False)

    plan_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("plans.id"))
    billing_status = db.Column(db.String(20), default="TRIAL")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
