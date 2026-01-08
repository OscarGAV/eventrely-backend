import os
from datetime import datetime, timedelta, timezone
from typing import Any
import jwt
from jwt.exceptions import InvalidTokenError


class JWTService:
    """
    Service for JWT token generation and validation
    """

    def __init__(self):
        # Get secret from environment or use default (change in production!)
        self.secret_key = os.environ.get("JWT_SECRET_KEY", "your-secret-key-change-this")
        self.algorithm = "HS256"
        self.access_token_expire_minutes = 30  # 30 minutes
        self.refresh_token_expire_days = 7  # 7 days

    def create_access_token(self, user_id: int, username: str, email: str, role: str) -> str:
        """
        Create JWT access token
        """
        expire = datetime.now(timezone.utc) + timedelta(minutes=self.access_token_expire_minutes)

        payload = {
            "sub": str(user_id),  # Subject (user_id)
            "username": username,
            "email": email,
            "role": role,  # Include role in token
            "type": "access",
            "exp": expire,
            "iat": datetime.now(timezone.utc)
        }

        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token

    def create_refresh_token(self, user_id: int) -> str:
        """
        Create JWT refresh token (longer expiration)
        """
        expire = datetime.now(timezone.utc) + timedelta(days=self.refresh_token_expire_days)

        payload = {
            "sub": str(user_id),
            "type": "refresh",
            "exp": expire,
            "iat": datetime.now(timezone.utc)
        }

        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token

    def verify_token(self, token: str) -> dict[str, Any]:
        """
        Verify and decode JWT token
        Raises InvalidTokenError if token is invalid or expired
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except InvalidTokenError as e:
            raise ValueError(f"Invalid token: {str(e)}")

    def get_user_id_from_token(self, token: str) -> int:
        """
        Extract user_id from token
        """
        payload = self.verify_token(token)
        return int(payload["sub"])

    def is_token_expired(self, token: str) -> bool:
        """
        Check if token is expired
        """
        try:
            self.verify_token(token)
            return False
        except ValueError:
            return True


# Singleton instance
jwt_service = JWTService()