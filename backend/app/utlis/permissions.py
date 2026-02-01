from flask_jwt_extended import get_jwt

def require_role(required_role):
    claims = get_jwt()
    return claims.get("role") == required_role
