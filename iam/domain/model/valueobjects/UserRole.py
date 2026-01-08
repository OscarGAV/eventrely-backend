from dataclasses import dataclass
from enum import Enum


class UserRoleEnum(str, Enum):
    """Enum for user roles"""
    GENERAL = "general_user"
    ADMIN = "admin_user"


@dataclass(frozen=True)
class UserRole:
    """
    Value Object: User Role
    Encapsulates role validation and behavior
    """
    value: UserRoleEnum

    def __post_init__(self):
        if not isinstance(self.value, UserRoleEnum):
            raise ValueError(f"Invalid role: {self.value}")

    def is_admin(self) -> bool:
        """Check if role is admin"""
        return self.value == UserRoleEnum.ADMIN

    def is_general(self) -> bool:
        """Check if role is general user"""
        return self.value == UserRoleEnum.GENERAL

    def can_view_all_events(self) -> bool:
        """Check if user can view all events (admin privilege)"""
        return self.is_admin()

    def can_manage_users(self) -> bool:
        """Check if user can manage other users (admin privilege)"""
        return self.is_admin()

    def __str__(self) -> str:
        return self.value.value

    @staticmethod
    def default() -> 'UserRole':
        """Default role for new users"""
        return UserRole(UserRoleEnum.GENERAL)

    @staticmethod
    def from_string(role_str: str) -> 'UserRole':
        """Create UserRole from string"""
        try:
            return UserRole(UserRoleEnum(role_str))
        except ValueError:
            raise ValueError(f"Invalid role string: {role_str}")