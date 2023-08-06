from gettext import gettext as _
from typing import AsyncGenerator, Dict, Optional, Type, Union, cast

from fastapi import Depends, Request
from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi_users import BaseUserManager, InvalidPasswordException
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    Strategy,
)
from fastapi_users.manager import UserNotExists
from fastapi_users_db_sqlalchemy import (
    SQLAlchemyBaseOAuthAccountTable,
    SQLAlchemyBaseUserTable,
    SQLAlchemyUserDatabase,
)
from jwcrypto import jwk
from sqlalchemy.sql import Select

from fief.crypto.access_token import InvalidAccessToken, read_access_token
from fief.db import AsyncSession
from fief.dependencies.account import get_current_account_session
from fief.dependencies.tenant import get_current_tenant
from fief.models import Tenant, User
from fief.schemas.user import UserCreate, UserCreateInternal, UserDB


class UserManager(BaseUserManager[UserCreate, UserDB]):
    user_db_model = UserDB
    reset_password_token_secret = "SECRET"
    verification_token_secret = "SECRET"

    def __init__(self, user_db: SQLAlchemyUserDatabase[UserDB], tenant: Tenant):
        super().__init__(user_db)
        self.tenant = tenant

    async def validate_password(
        self, password: str, user: Union[UserCreate, UserDB]
    ) -> None:
        if len(password) < 8:
            raise InvalidPasswordException(
                reason=_("The password should be at least 8 characters.")
            )

    async def create(
        self, user: UserCreate, safe: bool = False, request: Optional[Request] = None
    ) -> UserDB:
        user_dict = (
            user.create_update_dict() if safe else user.create_update_dict_superuser()
        )
        user_create = UserCreateInternal(**user_dict, tenant_id=self.tenant.id)
        return await super().create(user_create, safe=safe, request=request)

    async def on_after_register(self, user: UserDB, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: UserDB, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: UserDB, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")


class SQLAlchemyUserTenantDatabase(SQLAlchemyUserDatabase[UserDB]):
    def __init__(
        self,
        user_db_model: Type[UserDB],
        session: AsyncSession,
        tenant: Tenant,
        user_table: Type[User],
        oauth_account_table: Optional[Type[SQLAlchemyBaseOAuthAccountTable]] = None,
    ):
        super().__init__(
            user_db_model,
            session,
            cast(Type[SQLAlchemyBaseUserTable], user_table),
            oauth_account_table=oauth_account_table,
        )
        self.tenant = tenant

    async def _get_user(self, statement: Select) -> Optional[UserDB]:
        statement = statement.where(User.tenant_id == self.tenant.id)
        return await super()._get_user(statement)


class JWTAccessTokenStrategy(Strategy[UserCreate, UserDB]):
    def __init__(self, key: jwk.JWK):
        self.key = key

    async def read_token(
        self, token: Optional[str], user_manager: BaseUserManager[UserCreate, UserDB]
    ) -> Optional[UserDB]:
        if token is None:
            return None

        try:
            user_id = read_access_token(self.key, token)
            user = await user_manager.get(user_id)
        except InvalidAccessToken:
            return None
        except UserNotExists:
            return None
        else:
            return user


async def get_jwt_access_token_strategy(
    tenant: Tenant = Depends(get_current_tenant),
) -> JWTAccessTokenStrategy:
    return JWTAccessTokenStrategy(tenant.get_sign_jwk())


async def get_user_db(
    session: AsyncSession = Depends(get_current_account_session),
    tenant: Tenant = Depends(get_current_tenant),
) -> AsyncGenerator[SQLAlchemyUserDatabase[UserDB], None]:
    yield SQLAlchemyUserTenantDatabase(UserDB, session, tenant, User)


async def get_user_manager(
    user_db: SQLAlchemyUserDatabase[UserDB] = Depends(get_user_db),
    tenant: Tenant = Depends(get_current_tenant),
):
    yield UserManager(user_db, tenant)


class AuthorizationCodeBearerTransport(BearerTransport):
    scheme: OAuth2AuthorizationCodeBearer  # type: ignore

    def __init__(
        self,
        authorizationUrl: str,
        tokenUrl: str,
        refreshUrl: str,
        scopes: Dict[str, str],
    ):
        self.scheme = OAuth2AuthorizationCodeBearer(
            authorizationUrl, tokenUrl, refreshUrl, scopes=scopes
        )


authentication_backend = AuthenticationBackend[UserCreate, UserDB](
    "jwt_access_token",
    AuthorizationCodeBearerTransport(
        "/authorize", "/token", "/token", {"openid": "openid"}
    ),
    get_jwt_access_token_strategy,
)
