from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.admin_user import AdminUser


class CRUDAdminUser:
    async def get_by_username(self, session: AsyncSession, username: str) -> AdminUser | None:
        result = await session.execute(select(AdminUser).where(AdminUser.username == username))
        return result.scalar_one_or_none()

    async def get(self, session: AsyncSession, admin_user_id: int) -> AdminUser | None:
        result = await session.execute(select(AdminUser).where(AdminUser.id == admin_user_id))
        return result.scalar_one_or_none()

    async def create(
        self,
        session: AsyncSession,
        *,
        username: str,
        password_hash: str,
        is_superuser: bool = False,
        is_active: bool = True,
    ) -> AdminUser:
        obj = AdminUser(
            username=username,
            password_hash=password_hash,
            is_superuser=is_superuser,
            is_active=is_active,
        )
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj

    async def set_last_login(self, session: AsyncSession, obj: AdminUser) -> None:
        obj.last_login_at = datetime.utcnow()
        await session.commit()


crud_admin_user = CRUDAdminUser()
