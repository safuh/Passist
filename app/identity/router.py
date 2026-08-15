from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.identity.models import User
from app.identity.schemas import (
    LoginRequest,
    RefreshRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)
from app.identity.service import (
    AuthenticationError,
    AuthenticationService,
    RegistrationError,
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    data: RegisterRequest,
    db: AsyncSession = Depends(get_db),
):
    service = AuthenticationService(db)

    try:
        user = await service.register(
            email=data.email,
            username=data.username,
            password=data.password,
        )

        return user

    except RegistrationError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        )


@router.post(
    "/login",
    response_model=TokenResponse,
)
async def login(
    data: LoginRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    service = AuthenticationService(db)

    user_agent = request.headers.get("user-agent")

    ip_address = (
        request.client.host
        if request.client
        else None
    )

    try:
        (
            access_token,
            refresh_token,
            expires_in,
        ) = await service.authenticate(
            email=data.email,
            password=data.password,
            user_agent=user_agent,
            ip_address=ip_address,
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=expires_in,
        )

    except AuthenticationError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
            headers={
                "WWW-Authenticate": "Bearer",
            },
        )


@router.post(
    "/refresh",
    response_model=TokenResponse,
)
async def refresh(
    data: RefreshRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    service = AuthenticationService(db)

    user_agent = request.headers.get("user-agent")

    ip_address = (
        request.client.host
        if request.client
        else None
    )

    try:
        (
            access_token,
            refresh_token,
            expires_in,
        ) = await service.refresh(
            refresh_token=data.refresh_token,
            user_agent=user_agent,
            ip_address=ip_address,
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=expires_in,
        )

    except AuthenticationError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
            headers={
                "WWW-Authenticate": "Bearer",
            },
        )


@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def logout(
    data: RefreshRequest,
    db: AsyncSession = Depends(get_db),
):
    service = AuthenticationService(db)

    await service.logout(
        refresh_token=data.refresh_token,
    )


@router.get(
    "/me",
    response_model=UserResponse,
)
async def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user