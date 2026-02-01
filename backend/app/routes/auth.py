from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
)
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db
from app.models.user import User
from app.models.company import Company
from app.models.role import Role

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    required_fields = [
        "company_name",
        "email",
        "password",
        "confirm_password",
    ]

    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    if data["password"] != data["confirm_password"]:
        return jsonify({"error": "Passwords do not match"}), 400

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already registered"}), 409

    # Create company
    company = Company(name=data["company_name"])
    db.session.add(company)

    # Assign ADMIN role to first user
    admin_role = Role.query.filter_by(name="ADMIN").first()

    user = User(
        email=data["email"],
        password_hash=generate_password_hash(data["password"]),
        company_id=company.id,
        role_id=admin_role.id,
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Registration successful"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    user = User.query.filter_by(email=data.get("email")).first()

    if not user or not check_password_hash(
        user.password_hash, data.get("password")
    ):
        return jsonify({"error": "Invalid email or password"}), 401

    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={
            "company_id": str(user.company_id),
            "role": user.role.name,
        },
    )

    return jsonify(access_token=access_token), 200


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    return jsonify(
        {
            "id": str(user.id),
            "email": user.email,
            "company_id": str(user.company_id),
            "role_id": str(user.role_id),
        }
    )
