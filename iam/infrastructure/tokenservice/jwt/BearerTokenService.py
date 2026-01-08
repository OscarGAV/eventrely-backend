from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from iam.application.internal.tokenservice.JWTService import jwt_service
from iam.infrastructure.persistence.repositories.UserRepositoryImpl import UserRepositoryImpl
from shared.infrastructure.persistence.configuration.database_configuration import get_db_session
from iam.domain.model.aggregates.User import User

# Security scheme for Swagger UI
security = HTTPBearer()


async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: AsyncSession = Depends(get_db_session)
) -> User:
    """
    FastAPI dependency to get current authenticated user from JWT token

    Usage in endpoints:
        @router.get("/protected")
        async def protected_route(current_user: User = Depends(get_current_user)):
            return {"user_id": current_user.id}
    """

    token = credentials.credentials

    try:
        # Verify and decode token
        user_id = jwt_service.get_user_id_from_token(token)

        # Get user from database
        repository = UserRepositoryImpl(db)
        user = await repository.find_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"}
            )

        if not user.can_authenticate():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Account is deactivated",
                headers={"WWW-Authenticate": "Bearer"}
            )

        return user

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"}
        )


async def get_current_active_user(
        current_user: User = Depends(get_current_user)
) -> User:
    """
    Get current user and ensure account is active
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is not active"
        )
    return current_user


async def get_current_admin_user(
        current_user: User = Depends(get_current_active_user)
) -> User:
    """
    Get current user and ensure they have admin role

    Usage:
        @router.get("/admin-only")
        async def admin_route(admin_user: User = Depends(get_current_admin_user)):
            return {"message": "Admin access granted"}
    """
    if not current_user.is_admin():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user


async def get_current_general_user(
        current_user: User = Depends(get_current_active_user)
) -> User:
    """
    Get current user and ensure they have general user role

    Usage:
        @router.post("/general-only")
        async def general_route(user: User = Depends(get_current_general_user)):
            return {"message": "General user access"}
    """
    if not current_user.is_general_user():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This action is only available for general users"
        )
    return current_user


def get_user_id_from_token_dependency(
        credentials: HTTPAuthorizationCredentials = Depends(security)
) -> int:
    """
    Extract user_id from token without database lookup
    Useful for lightweight operations
    """
    token = credentials.credentials
    try:
        return jwt_service.get_user_id_from_token(token)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"}
        )