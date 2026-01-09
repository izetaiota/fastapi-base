from __future__ import annotations

from datetime import datetime, timedelta, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.exceptions import BusinessError
from security.jwt import jwt_encode
from utils.password import hash_password, verify_password

from modules.admin_user.crud import crud_admin_user


class AdminAuthError(BusinessError):
    code: str = "ADMIN_AUTH_ERROR"
    pass


class AdminUserService:
    async def register(
        self,
        session: AsyncSession,
        *,
        username: str,
        password: str,
        is_superuser: bool = False,
    ):
        existing = await crud_admin_user.get_by_username(session, username)
        if existing is not None:
            raise AdminAuthError("username already exists")

        password_hash = hash_password(password)
        return await crud_admin_user.create(
            session,
            username=username,
            password_hash=password_hash,
            is_superuser=is_superuser,
        )

    async def authenticate(self, session: AsyncSession, *, username: str, password: str):
        user = await crud_admin_user.get_by_username(session, username)
        if user is None:
            raise AdminAuthError("invalid credentials")
        if not user.is_active:
            raise AdminAuthError("user is inactive")
        if not verify_password(password, user.password_hash):
            raise AdminAuthError("invalid credentials")

        await crud_admin_user.set_last_login(session, user)
        return user

    def issue_access_token(self, *, admin_user_id: int) -> str:
        now = datetime.now(tz=timezone.utc)
        exp = now + timedelta(minutes=settings.admin_access_token_expire_minutes)
        payload = {
            "sub": str(admin_user_id),
            "typ": "admin",
            "iat": int(now.timestamp()),
            "exp": int(exp.timestamp()),
        }
        return jwt_encode(payload)


admin_user_service = AdminUserService()
