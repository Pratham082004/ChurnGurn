from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt
import uuid

from app.extensions import db
from app.models.api_key import APIKey
from app.utlis.rbac import require_roles

api_keys_bp = Blueprint("api_keys", __name__)

@api_keys_bp.route("/create", methods=["POST"])
@jwt_required()
@require_roles("ADMIN")
def create_api_key():
    claims = get_jwt()
    company_id = claims.get("company_id")

    api_key = APIKey(
        company_id=company_id,
        key=uuid.uuid4().hex
    )

    db.session.add(api_key)
    db.session.commit()

    return jsonify({
        "api_key": api_key.key,
        "message": "Store this key securely. It will not be shown again."
    }), 201

@api_keys_bp.route("/<uuid:key_id>/disable", methods=["POST"])
@jwt_required()
@require_roles("ADMIN")
def disable_api_key(key_id):
    claims = get_jwt()
    company_id = claims.get("company_id")

    api_key = APIKey.query.filter_by(
        id=key_id,
        company_id=company_id
    ).first_or_404()

    api_key.is_active = False
    db.session.commit()

    return jsonify({"message": "API key disabled"})
