from functools import wraps
from flask import request, jsonify, g
from app.models.api_key import APIKey

def require_api_key(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        api_key = request.headers.get("x-api-key")

        if not api_key:
            return jsonify({"error": "API key missing"}), 401

        key_record = APIKey.query.filter_by(
            key=api_key,
            is_active=True
        ).first()

        if not key_record:
            return jsonify({"error": "Invalid API key"}), 403

        # Attach company_id to request context
        g.company_id = key_record.company_id

        return fn(*args, **kwargs)
    return wrapper
