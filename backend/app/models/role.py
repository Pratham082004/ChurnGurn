from app.extensions import db
from app.models.base import UUIDMixin

class Role(UUIDMixin, db.Model):
    __tablename__ = "roles"

    name = db.Column(db.String(50), unique=True, nullable=False)
    # ADMIN, ANALYST, VIEWER
