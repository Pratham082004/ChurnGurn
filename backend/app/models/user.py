from datetime import datetime
from app.extensions import db
from app.models.base import UUIDMixin

class User(UUIDMixin, db.Model):
    __tablename__ = "users"

    company_id = db.Column(
        db.UUID(as_uuid=True),
        db.ForeignKey("companies.id"),
        nullable=False
    )
    role_id = db.Column(
        db.UUID(as_uuid=True),
        db.ForeignKey("roles.id"),
        nullable=False
    )

    role = db.relationship("Role")  # 🔥 ADD THIS LINE

    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
