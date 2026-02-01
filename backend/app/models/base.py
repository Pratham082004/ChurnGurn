# app/models/base.py
import uuid
from app.extensions import db

class UUIDMixin:
    id = db.Column(
        db.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
