"""
Authentication service
"""
from datetime import timedelta
from typing import Optional
from app.models.user import User
from app.core.security import verify_password, get_password_hash, create_access_token
from app.core.config import settings


class AuthService:
    """Authentication service"""

    @staticmethod
    async def authenticate_user(username: str, password: str) -> Optional[User]:
        """
        Authenticate user by username and password
        Returns User if authentication successful, None otherwise
        """
        user = await User.find_one(User.username == username)
        if not user:
            return None

        if not verify_password(password, user.password_hash):
            return None

        return user

    @staticmethod
    async def create_user(
        username: str,
        email: str,
        password: str,
        role: str = "user"
    ) -> User:
        """Create a new user"""
        password_hash = get_password_hash(password)

        user = User(
            username=username,
            email=email,
            password_hash=password_hash,
            role=role
        )

        await user.insert()
        return user

    @staticmethod
    def create_token_for_user(user: User) -> dict:
        """Create access token for user"""
        access_token_expires = timedelta(
            minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )

        access_token = create_access_token(
            data={"sub": str(user.id)},
            expires_delta=access_token_expires
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }

    @staticmethod
    async def get_user_by_username(username: str) -> Optional[User]:
        """Get user by username"""
        return await User.find_one(User.username == username)

    @staticmethod
    async def get_user_by_email(email: str) -> Optional[User]:
        """Get user by email"""
        return await User.find_one(User.email == email)
