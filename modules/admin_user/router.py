from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps import db_session
from core.config import settings

from modules.admin_user.schemas import AdminLoginRequest, AdminMeResponse, AdminRegisterRequest, AdminTokenResponse
from modules.admin_user.service import AdminAuthError, admin_user_service
from app.deps import current_admin_user

router = APIRouter(prefix="/admin")


@router.post("/login", response_model=AdminTokenResponse)
async def login(payload: AdminLoginRequest, session: AsyncSession = Depends(db_session)):
    try:
        user = await admin_user_service.authenticate(session, username=payload.username, password=payload.password)
    except AdminAuthError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc))
    token = admin_user_service.issue_access_token(admin_user_id=user.id)
    return AdminTokenResponse(access_token=token)


@router.post("/register", response_model=AdminMeResponse)
async def register(
    payload: AdminRegisterRequest,
    x_admin_bootstrap_token: str | None = Header(default=None, alias="X-Admin-Bootstrap-Token"),
    session: AsyncSession = Depends(db_session),
):
    if settings.admin_bootstrap_token and x_admin_bootstrap_token != settings.admin_bootstrap_token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid bootstrap token")

    user = await admin_user_service.register(
        session,
        username=payload.username,
        password=payload.password,
        is_superuser=payload.is_superuser,
    )
    return AdminMeResponse(
        id=user.id,
        username=user.username,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
    )


@router.get("/me", response_model=AdminMeResponse)
async def me(user=Depends(current_admin_user)):
    return AdminMeResponse(
        id=user.id,
        username=user.username,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
    )
