from fastapi import Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db


async def db_session(session: AsyncSession = Depends(get_db)) -> AsyncSession:
    return session


async def request_id(x_request_id: str | None = Header(default=None, alias="X-Request-ID")) -> str | None:
    return x_request_id
