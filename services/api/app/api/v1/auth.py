from fastapi import APIRouter
from app.schemas.auth import LoginRequest, Token
from app.services.auth_service import auth_service

router = APIRouter()


@router.post(
    "/auth/login",
    response_model=Token,
    summary="User & Driver authentication",
    description="Authenticates driver or admin user and returns JWT bearer token."
)
async def login(req: LoginRequest):
    return await auth_service.login(req)
