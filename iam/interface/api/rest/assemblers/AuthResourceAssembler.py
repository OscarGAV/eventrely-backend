from iam.domain.model.commands.UserCommands import (
    SignUpCommand,
    SignInCommand,
    ChangePasswordCommand,
    UpdateProfileCommand,
    DeactivateUserCommand
)
from iam.domain.model.queries.UserQueries import (
    GetUserByIdQuery,
    GetUserByUsernameQuery,
    GetUserByEmailQuery,
    GetAllUsersQuery
)
from iam.domain.model.aggregates.User import User
from iam.interface.api.rest.resources.AuthRequestResource import (
    SignUpRequest,
    SignInRequest,
    ChangePasswordRequest,
    UpdateProfileRequest
)
from iam.interface.api.rest.resources.AuthResponseResource import (
    UserResponse,
    AuthenticationResponse as AuthResponseDTO,
    UserListResponse
)
from iam.application.internal.commandservice.CommandServiceImpl import AuthenticationResponse


class AuthResourceAssembler:
    """
    Assembler to transform between presentation and domain layers
    """

    # =========================================================================
    # Request → Command
    # =========================================================================

    @staticmethod
    def to_sign_up_command(request: SignUpRequest) -> SignUpCommand:
        """Convert SignUpRequest → SignUpCommand"""
        return SignUpCommand(
            username=request.username,
            email=request.email,
            password=request.password,
            role=request.role,
            full_name=request.full_name
        )

    @staticmethod
    def to_sign_in_command(request: SignInRequest) -> SignInCommand:
        """Convert SignInRequest → SignInCommand"""
        return SignInCommand(
            username_or_email=request.username_or_email,
            password=request.password
        )

    @staticmethod
    def to_change_password_command(user_id: int, request: ChangePasswordRequest) -> ChangePasswordCommand:
        """Convert ChangePasswordRequest → ChangePasswordCommand"""
        return ChangePasswordCommand(
            user_id=user_id,
            old_password=request.old_password,
            new_password=request.new_password
        )

    @staticmethod
    def to_update_profile_command(user_id: int, request: UpdateProfileRequest) -> UpdateProfileCommand:
        """Convert UpdateProfileRequest → UpdateProfileCommand"""
        return UpdateProfileCommand(
            user_id=user_id,
            full_name=request.full_name,
            email=request.email
        )

    @staticmethod
    def to_deactivate_command(user_id: int) -> DeactivateUserCommand:
        """Create DeactivateUserCommand"""
        return DeactivateUserCommand(user_id=user_id)

    # =========================================================================
    # Params → Query
    # =========================================================================

    @staticmethod
    def to_get_by_id_query(user_id: int) -> GetUserByIdQuery:
        """Create GetUserByIdQuery"""
        return GetUserByIdQuery(user_id=user_id)

    @staticmethod
    def to_get_by_username_query(username: str) -> GetUserByUsernameQuery:
        """Create GetUserByUsernameQuery"""
        return GetUserByUsernameQuery(username=username)

    @staticmethod
    def to_get_by_email_query(email: str) -> GetUserByEmailQuery:
        """Create GetUserByEmailQuery"""
        return GetUserByEmailQuery(email=email)

    @staticmethod
    def to_get_all_query() -> GetAllUsersQuery:
        """Create GetAllUsersQuery"""
        return GetAllUsersQuery()

    # =========================================================================
    # Domain → Response
    # =========================================================================

    @staticmethod
    def to_user_response(user: User) -> UserResponse:
        """Convert User → UserResponse"""
        return UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            role=user.role,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at
        )

    @staticmethod
    def to_authentication_response(auth_response: AuthenticationResponse) -> AuthResponseDTO:
        """Convert AuthenticationResponse → AuthenticationResponseDTO"""
        return AuthResponseDTO(
            user=AuthResourceAssembler.to_user_response(auth_response.user),
            access_token=auth_response.access_token,
            refresh_token=auth_response.refresh_token,
            token_type="Bearer"
        )

    @staticmethod
    def to_user_list_response(users: list[User]) -> UserListResponse:
        """Convert list[User] → UserListResponse"""
        return UserListResponse(
            users=[AuthResourceAssembler.to_user_response(u) for u in users],
            total=len(users)
        )