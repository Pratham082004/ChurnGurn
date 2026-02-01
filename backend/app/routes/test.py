from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from app.utlis.rbac import require_roles

test_bp = Blueprint("test", __name__)

@test_bp.route("/admin-only", methods=["GET"])
@jwt_required()
@require_roles("ADMIN")
def admin_only():
    return jsonify({"message": "Welcome ADMIN 🚀"})
